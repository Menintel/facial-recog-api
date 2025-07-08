from fastapi import APIRouter, Depends
from backend.services.deepface_service.schemas.deepface_schemas import VerifyRequest, VerifyResponse
from backend.services.deepface_service.services.deepface_service import verify_faces
from backend.services.deepface_service.dependencies.auth_deps import get_current_user_from_auth_service

recognition_router = APIRouter(prefix="/recognize", tags=["Recognition"])

@recognition_router.post("/verify", response_model=VerifyResponse)
async def verify_faces_endpoint(
    request: VerifyRequest,
    current_user: dict = Depends(get_current_user_from_auth_service) # Protected endpoint
):
    result = await verify_faces(
        request.image_base64_1,
        request.image_base64_2,
        request.model_name,
        request.detector_backend,
        request.distance_metric
    )
    return VerifyResponse(**result)