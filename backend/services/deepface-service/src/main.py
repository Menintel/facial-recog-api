from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.services.deepface_service.routers import detection, recognition, analysis
from backend.services.deepface_service.services.model_manager import ModelManager
from backend.shared.constants.api_constants import API_PREFIX
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("DeepFace Service starting up. Initializing models...")
    # ModelManager.initialize() # DeepFace downloads models on first use,
                               # so this explicit call might not be needed
                               # unless you want to pre-load specific models.
                               # For large models, this can cause long startup.
    logger.info("DeepFace Service startup complete.")
    yield
    # Shutdown logic would go here if needed this is not needed for now @Menintel
    logger.info("DeepFace Service shutting down...")

app = FastAPI(
    title="DeepFace Service",
    description="Facial Detection, Recognition, and Analysis API using DeepFace",
    version="0.1.0",
    openapi_url=f"{API_PREFIX}/deepface/openapi.json",
    docs_url=f"{API_PREFIX}/deepface/docs",
    redoc_url=f"{API_PREFIX}/deepface/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detection.detection_router, prefix=API_PREFIX)
app.include_router(recognition.recognition_router, prefix=API_PREFIX)
app.include_router(analysis.analysis_router, prefix=API_PREFIX)



@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "DeepFace Service is running!"}