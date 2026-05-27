from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.prediction_record import PredictionRecord

router = APIRouter()

@router.get("/doctor/high-risk")
def get_high_risk_patients(db: Session = Depends(get_db)):
    records = (
        db.query(PredictionRecord)
        .filter(PredictionRecord.risk_level == "High Risk")
        .order_by(PredictionRecord.created_at.desc())
        .all()
    )

    return [
        {
            "patient_name": r.patient_name,
            "age": r.age,
            "glucose": r.glucose,
            "bmi": r.bmi,
            "probability": r.probability,
            "risk_level": r.risk_level,
            "health_score": r.health_score,
            "recommendation": r.recommendation,
            "created_at": r.created_at
        }
        for r in records
    ]

@router.get("/doctor/patient/{patient_name}")
def get_patient_summary(patient_name: str, db: Session = Depends(get_db)):
    records = (
        db.query(PredictionRecord)
        .filter(PredictionRecord.patient_name.ilike(f"%{patient_name}%"))
        .order_by(PredictionRecord.created_at.desc())
        .all()
    )

    if not records:
        return {"message": "No records found for this patient."}

    latest = records[0]

    return {
        "patient_name": latest.patient_name,
        "latest_risk_level": latest.risk_level,
        "latest_probability": latest.probability,
        "latest_health_score": latest.health_score,
        "total_records": len(records),
        "latest_recommendation": latest.recommendation,
        "timeline": [
            {
                "date": r.created_at,
                "glucose": r.glucose,
                "bmi": r.bmi,
                "risk_level": r.risk_level,
                "health_score": r.health_score
            }
            for r in records
        ]
    }
