from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import httpx # For making HTTP requests to auth service
from backend.shared.constants.api_constants import AUTH_SERVICE_URL, API_PREFIX
from backend.shared.exceptions.api_exceptions import UnauthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{AUTH_SERVICE_URL}{API_PREFIX}/auth/token")

async def get_current_user_from_auth_service(token: str = Depends(oauth2_scheme)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{AUTH_SERVICE_URL}{API_PREFIX}/users/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status() # Raise an exception for 4xx/5xx responses
            user_data = response.json()
            if not user_data.get("is_active"):
                raise UnauthorizedException(detail="Inactive user")
            return user_data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_401_UNAUTHORIZED:
                raise UnauthorizedException(detail="Invalid authentication credentials")
            elif e.response.status_code == status.HTTP_403_FORBIDDEN:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
            else:
                raise HTTPException(status_code=e.response.status_code, detail=f"Auth service error: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Auth service unavailable: {e}")