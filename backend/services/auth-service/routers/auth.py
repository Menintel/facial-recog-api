from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.services.auth_service.schemas.auth_schemas import Token
from backend.services.auth_service.services.auth_service import verify_password, create_access_token, get_user_by_email, register_user
from backend.services.auth_service.schemas.user_schemas import UserCreate, UserResponse
from backend.shared.exceptions.api_exceptions import BadRequestException

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_new_user(user_data: UserCreate):
    try:
        user = register_user(user_data.email, user_data.password)
        return UserResponse(id=user.id, email=user.email, is_active=user.is_active)
    except ValueError as e:
        raise BadRequestException(detail=str(e))