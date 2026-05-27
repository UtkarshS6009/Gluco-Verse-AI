from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.prediction_schema import DiabetesPredictionRequest, DiabetesPredictionResponse
from app.models.prediction_record import PredictionRecord
from app.services.prediction_service import predict_diabetes_risk

router = APIRouter()

@router.post("/predict", response_model=DiabetesPredictionResponse)
def predict(payload: DiabetesPredictionRequest, db: Session = Depends(get_db)):
    try:
        result = predict_diabetes_risk(payload)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    record = PredictionRecord(
        patient_name=payload.patient_name,
        age=payload.age,
        pregnancies=payload.pregnancies or 0,
        glucose=payload.glucose,
        blood_pressure=payload.blood_pressure,
        skin_thickness=payload.skin_thickness,
        insulin=payload.insulin,
        bmi=payload.bmi,
        diabetes_pedigree_function=payload.diabetes_pedigree_function,
        probability=result["probability"],
        risk_level=result["risk_level"],
        health_score=result["health_score"],
        recommendation=result["recommendation"]
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return DiabetesPredictionResponse(
        patient_name=payload.patient_name,
        probability=result["probability"],
        risk_level=result["risk_level"],
        health_score=result["health_score"],
        recommendation=result["recommendation"],
        assistant_note=result["assistant_note"]
    )
