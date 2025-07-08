# backend/services/deepface-service/services/deepface_service.py
from deepface import DeepFace
import base64
import numpy as np
import cv2
from typing import List, Dict, Any, Optional
from backend.services.deepface_service.schemas.image_schemas import FaceDetectionResult, FaceAnalysisResult
from backend.shared.exceptions.api_exceptions import BadRequestException, NotFoundException
import logging

logger = logging.getLogger(__name__)

def _decode_image_base64(image_base64: str) -> np.ndarray:
    if "base64," in image_base64:
        header, image_base64 = image_base64.split("base64,")

    try:
        img_bytes = base64.b64decode(image_base64)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Could not decode image from base64.")
        return img
    except Exception as e:
        logger.error(f"Error decoding base64 image: {e}")
        raise BadRequestException(detail=f"Invalid image base64 string: {e}")

def _encode_image_base64(image_np: np.ndarray) -> str:
    _, buffer = cv2.imencode('.jpg', image_np)
    return base64.b64encode(buffer).decode('utf-8')

async def detect_faces(image_base64: str, detector_backend: str, return_face_chip: bool = True) -> List[FaceDetectionResult]:
    img = _decode_image_base64(image_base64)
    try:
        detections = DeepFace.extract_faces(
            img_path=img,
            detector_backend=detector_backend,
            enforce_detection=False, # Allow no faces detected without error
            align=True
        )
        results = []
        for det in detections:
            if det["facial_area"]:
                face_chip_base64 = None
                if return_face_chip and det.get("face"): # 'face' is the aligned face image
                    face_chip_base64 = _encode_image_base64(det["face"])

                results.append(FaceDetectionResult(
                    x=det["facial_area"]["x"],
                    y=det["facial_area"]["y"],
                    w=det["facial_area"]["w"],
                    h=det["facial_area"]["h"],
                    confidence=det["confidence"],
                    face_chip_base64=face_chip_base64
                ))
        return results
    except Exception as e:
        logger.error(f"DeepFace detection error: {e}")
        if "Face could not be detected" in str(e):
            return [] # No faces detected
        raise BadRequestException(detail=f"DeepFace detection failed: {e}")

async def verify_faces(image1_base64: str, image2_base64: str, model_name: str, detector_backend: str, distance_metric: str) -> Dict[str, Any]:
    img1 = _decode_image_base64(image1_base64)
    img2 = _decode_image_base64(image2_base64)
    try:
        result = DeepFace.verify(
            img1_path=img1,
            img2_path=img2,
            model_name=model_name,
            detector_backend=detector_backend,
            distance_metric=distance_metric,
            enforce_detection=True # Enforce detection for verification
        )
        return result
    except ValueError as e:
        if "Face could not be detected" in str(e):
            raise BadRequestException(detail="One or both faces could not be detected for verification.")
        raise BadRequestException(detail=f"DeepFace verification failed: {e}")
    except Exception as e:
        logger.error(f"DeepFace verification error: {e}")
        raise BadRequestException(detail=f"DeepFace verification failed: {e}")

async def analyze_faces(image_base64: str, detector_backend: str, actions: List[str], return_face_chip: bool = True) -> List[FaceAnalysisResult]:
    img = _decode_image_base64(image_base64)
    try:
        # DeepFace.analyze returns a list of dictionaries, one for each detected face
        analyses = DeepFace.analyze(
            img_path=img,
            actions=actions,
            detector_backend=detector_backend,
            enforce_detection=False, # Allow no faces detected without error
            align=True # Returns 'face' key in result
        )

        results = []
        for analysis in analyses:
            face_chip_base64 = None
            if return_face_chip and analysis.get("face"):
                face_chip_base64 = _encode_image_base64(analysis["face"])

            # DeepFace returns emotion as a dict with dominant_emotion
            # and gender as 'Man' or 'Woman'
            results.append(FaceAnalysisResult(
                emotion=analysis.get("dominant_emotion", "unknown"),
                dominant_emotion=analysis.get("dominant_emotion", "unknown"),
                emotion_scores=analysis.get("emotion", {}),
                age=analysis.get("age", 0),
                gender=analysis.get("gender", "unknown"),
                race=analysis.get("dominant_race", "unknown"),
                dominant_race=analysis.get("dominant_race", "unknown"),
                race_scores=analysis.get("race", {}),
                face_chip_base64=face_chip_base64
            ))
        return results
    except Exception as e:
        logger.error(f"DeepFace analysis error: {e}")
        if "Face could not be detected" in str(e):
            return [] # No faces detected
        raise BadRequestException(detail=f"DeepFace analysis failed: {e}")