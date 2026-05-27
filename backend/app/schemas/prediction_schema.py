from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DiabetesPredictionRequest(BaseModel):
    patient_name: str = Field(..., example="Rahul Sharma")
    age: int = Field(..., ge=1, le=120, example=35)
    pregnancies: Optional[int] = Field(0, ge=0, le=25, example=0)

    glucose: float = Field(..., ge=0, example=148)
    blood_pressure: float = Field(..., ge=0, example=72)
    skin_thickness: float = Field(..., ge=0, example=35)
    insulin: float = Field(..., ge=0, example=120)
    bmi: float = Field(..., ge=0, example=31.5)
    diabetes_pedigree_function: float = Field(..., ge=0, example=0.62)

class DiabetesPredictionResponse(BaseModel):
    patient_name: str
    probability: float
    risk_level: str
    health_score: float
    recommendation: str
    assistant_note: str

class PredictionHistoryResponse(BaseModel):
    id: int
    patient_name: str
    age: int
    pregnancies: int
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree_function: float
    probability: float
    risk_level: str
    health_score: float
    recommendation: str
    created_at: datetime

    class Config:
        from_attributes = True
