from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    role: str = "patient"

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class AssistantRequest(BaseModel):
    question: str
    risk_level: str | None = None

class AssistantResponse(BaseModel):
    answer: str
    source: str
