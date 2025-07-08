from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.services.auth_service.schemas.auth_schemas import TokenData
from backend.services.auth_service.services.auth_service import decode_access_token, get_user_by_email
from backend.shared.exceptions.api_exceptions import UnauthorizedException # Import from shared

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # Points to your /token endpoint

async def get_current_user(token: str = Depends(oauth2_scheme)):
    token_data = decode_access_token(token)
    if token_data is None:
        raise UnauthorizedException(detail="Could not validate credentials")
    user = get_user_by_email(token_data.email)
    if user is None:
        raise UnauthorizedException(detail="Could not validate credentials")
    return user

async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user