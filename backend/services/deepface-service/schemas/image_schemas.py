from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class ImageBase64(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image string (e.g., 'data:image/jpeg;base64,...' or just the base64 string)")

class FaceDetectionResult(BaseModel):
    x: int
    y: int
    w: int
    h: int
    confidence: float
    face_chip_base64: Optional[str] = None # Base64 of the detected face chip

class FaceRecognitionResult(BaseModel):
    is_identified: bool
    identity: Optional[str] = None
    similarity: Optional[float] = None
    face_chip_base64: Optional[str] = None # Base64 of the recognized face chip


class FaceAnalysisResult(BaseModel):
    emotion: str
    dominant_emotion: str
    emotion_scores: dict
    age: int
    gender: Literal["Man", "Woman"] # DeepFace outputs "Man" or "Woman"
    race: str
    dominant_race: str
    race_scores: dict
    face_chip_base64: Optional[str] = None