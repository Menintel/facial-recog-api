from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CoreModel(BaseModel):
    id: Optional[str] = None # UUID or similar
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True # Pydantic v2 equivalent of orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
