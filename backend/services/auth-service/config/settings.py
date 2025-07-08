from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@db:5432/auth_db"
    secret_key: str = "YOUR_SUPER_SECRET_KEY" # CHANGE THIS IN PRODUCTION
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
