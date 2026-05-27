from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.prediction_record import PredictionRecord
from app.schemas.prediction_schema import PredictionHistoryResponse

router = APIRouter()

@router.get("/history", response_model=List[PredictionHistoryResponse])
def get_all_history(db: Session = Depends(get_db)):
    return (
        db.query(PredictionRecord)
        .order_by(PredictionRecord.created_at.desc())
        .all()
    )

@router.get("/history/{patient_name}", response_model=List[PredictionHistoryResponse])
def get_patient_history(patient_name: str, db: Session = Depends(get_db)):
    return (
        db.query(PredictionRecord)
        .filter(PredictionRecord.patient_name.ilike(f"%{patient_name}%"))
        .order_by(PredictionRecord.created_at.desc())
        .all()
    )
