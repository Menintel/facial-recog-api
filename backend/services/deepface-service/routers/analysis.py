from fastapi import APIRouter, Depends
from backend.services.deepface_service.schemas.deepface_schemas import AnalyzeRequest, AnalyzeResponse
from backend.services.deepface_service.services.deepface_service import analyze_faces
from backend.services.deepface_service.dependencies.auth_deps import get_current_user_from_auth_service

analysis_router = APIRouter(prefix="/analyze", tags=["Analysis"])

@analysis_router.post("/", response_model=AnalyzeResponse)
async def analyze_faces_endpoint(
    request: AnalyzeRequest,
    current_user: dict = Depends(get_current_user_from_auth_service) # Protected endpoint
):
    analyses = await analyze_faces(request.image_base64, request.detector_backend, request.actions, request.return_face_chip)
    return {"analyses": analyses, "analyzed_faces_count": len(analyses)}