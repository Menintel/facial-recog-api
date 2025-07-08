from fastapi import APIRouter, Depends, HTTPException, status
from backend.services.deepface_service.schemas.deepface_schemas import DetectRequest, DetectResponse
from backend.services.deepface_service.services.deepface_service import detect_faces
from backend.services.deepface_service.dependencies.auth_deps import get_current_user_from_auth_service

detection_router = APIRouter(prefix="/detect", tags=["Detection"])

@detection_router.post("/", response_model=DetectResponse)
async def detect_faces_endpoint(
    request: DetectRequest,
    current_user: dict = Depends(get_current_user_from_auth_service) # Protected endpoint
):
    faces = await detect_faces(request.image_base64, request.detector_backend, request.return_face_chip)
    return {"faces": faces, "detected_faces_count": len(faces)}