from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.services.auth_service.config.settings import settings
from backend.services.auth_service.schemas.auth_schemas import TokenData
from backend.services.auth_service.models.user import User # In a real app, this would be a DB session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            return None
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
        return None

# Mock user database (replace with actual DB calls)
MOCK_USERS_DB = {
    "test@example.com": User(
        id="1",
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        is_active=True
    ),
    "admin": User(
        id="2",
        email="admin",
        hashed_password=get_password_hash("admin"),
        is_active=True
    )
}

def get_user_by_email(email: str) -> Optional[User]:
    return MOCK_USERS_DB.get(email)

def register_user(email: str, password: str) -> User:
    if get_user_by_email(email):
        raise ValueError("Email already registered")
    hashed_password = get_password_hash(password)
    new_user = User(
        id=str(len(MOCK_USERS_DB) + 1), # Simple ID generation
        email=email,
        hashed_password=hashed_password,
        is_active=True
    )
    MOCK_USERS_DB[email] = new_user
    return new_user