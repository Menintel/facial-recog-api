from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from backend.services.deepface_service.config.deepface_config import deepface_settings
from backend.services.deepface_service.schemas.image_schemas import ImageBase64

class DetectRequest(ImageBase64):
    detector_backend: Literal[tuple(deepface_settings.supported_detectors)] = deepface_settings.default_detector_backend
    return_face_chip: bool = True

class DetectResponse(BaseModel):
    faces: List[FaceDetectionResult]
    detected_faces_count: int

class VerifyRequest(BaseModel):
    image_base64_1: str = Field(..., description="Base64 encoded image 1")
    image_base64_2: str = Field(..., description="Base64 encoded image 2")
    model_name: Literal[tuple(deepface_settings.supported_models)] = deepface_settings.default_model_name
    detector_backend: Literal[tuple(deepface_settings.supported_detectors)] = deepface_settings.default_detector_backend
    distance_metric: str = deepface_settings.default_distance_metric

class VerifyResponse(BaseModel):
    verified: bool
    distance: float
    threshold: float
    model_name: str
    detector_backend: str
    similarity_metric: str

class AnalyzeRequest(ImageBase64):
    detector_backend: Literal[tuple(deepface_settings.supported_detectors)] = deepface_settings.default_detector_backend
    actions: List[Literal["emotion", "age", "gender", "race"]] = ["emotion", "age", "gender", "race"]
    return_face_chip: bool = True

class AnalyzeResponse(BaseModel):
    analyses: List[FaceAnalysisResult]
    analyzed_faces_count: int