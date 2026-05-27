from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.prediction_record import PredictionRecord

def get_admin_overview(db: Session) -> dict:
    total_predictions = db.query(PredictionRecord).count()
    high_risk_count = db.query(PredictionRecord).filter(
        PredictionRecord.risk_level == "High Risk"
    ).count()

    avg_glucose = db.query(func.avg(PredictionRecord.glucose)).scalar() or 0
    avg_bmi = db.query(func.avg(PredictionRecord.bmi)).scalar() or 0
    avg_health_score = db.query(func.avg(PredictionRecord.health_score)).scalar() or 0

    return {
        "total_predictions": total_predictions,
        "high_risk_count": high_risk_count,
        "average_glucose": round(float(avg_glucose), 2),
        "average_bmi": round(float(avg_bmi), 2),
        "average_health_score": round(float(avg_health_score), 2)
    }

def get_risk_distribution(db: Session) -> dict:
    rows = db.query(
        PredictionRecord.risk_level,
        func.count(PredictionRecord.id)
    ).group_by(PredictionRecord.risk_level).all()

    return {risk: count for risk, count in rows}

def get_health_trends(db: Session, patient_name: str | None = None) -> list:
    query = db.query(PredictionRecord)

    if patient_name:
        query = query.filter(PredictionRecord.patient_name.ilike(f"%{patient_name}%"))

    records = query.order_by(PredictionRecord.created_at.asc()).all()

    return [
        {
            "patient_name": r.patient_name,
            "glucose": r.glucose,
            "bmi": r.bmi,
            "probability": r.probability,
            "risk_level": r.risk_level,
            "health_score": r.health_score,
            "created_at": r.created_at
        }
        for r in records
    ]
