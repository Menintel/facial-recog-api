from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.services.auth_service.routers import auth, users
from backend.shared.constants.api_constants import API_PREFIX

app = FastAPI(
    title="Auth Service",
    description="Authentication and User Management API",
    version="0.1.0",
    openapi_url=f"{API_PREFIX}/auth/openapi.json",
    docs_url=f"{API_PREFIX}/auth/docs",
    redoc_url=f"{API_PREFIX}/auth/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.auth_router, prefix=API_PREFIX)
app.include_router(users.users_router, prefix=API_PREFIX)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Auth Service is running!"}