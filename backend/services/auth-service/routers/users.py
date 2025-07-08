from fastapi import APIRouter, Depends
from backend.services.auth_service.dependencies.auth_deps import get_current_active_user
from backend.services.auth_service.schemas.user_schemas import UserResponse

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_active_user)):
    return UserResponse(id=current_user.id, email=current_user.email, is_active=current_user.is_active)