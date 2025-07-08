from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class DeepFaceSettings(BaseSettings):
    # Default models DeepFace will use
    default_model_name: str = "VGG-Face"
    default_detector_backend: str = "opencv"
    default_distance_metric: str = "cosine"
    # List of supported models and backends
    supported_models: List[str] = ["VGG-Face", "Facenet", "OpenFace", "DeepID", "ArcFace", "Dlib", "SFace"]
    supported_detectors: List[str] = ["opencv", "mtcnn", "retinaface", "mediapipe", "dlib", "yolov8"]

    # Whether to download models on startup or on first use (DeepFace handles this)
    # For production, pre-download models to models/ directory in Dockerfile or mount volume
    # DEEPFACE_HOME = "/app/models/.deepface" # DeepFace's default model download path : Menintel = Dont forget

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

deepface_settings = DeepFaceSettings()