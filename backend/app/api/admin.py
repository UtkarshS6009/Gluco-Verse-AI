from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.analytics_service import (
    get_admin_overview,
    get_risk_distribution,
    get_health_trends
)

router = APIRouter()

@router.get("/admin/overview")
def admin_overview(db: Session = Depends(get_db)):
    return get_admin_overview(db)

@router.get("/admin/risk-distribution")
def risk_distribution(db: Session = Depends(get_db)):
    return get_risk_distribution(db)

@router.get("/admin/health-trends")
def health_trends(patient_name: str | None = None, db: Session = Depends(get_db)):
    return get_health_trends(db, patient_name)
