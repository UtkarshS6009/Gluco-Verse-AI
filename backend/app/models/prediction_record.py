from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.db.database import Base

class PredictionRecord(Base):
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True)

    patient_name = Column(String, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    pregnancies = Column(Integer, default=0)

    glucose = Column(Float, nullable=False)
    blood_pressure = Column(Float, nullable=False)
    skin_thickness = Column(Float, nullable=False)
    insulin = Column(Float, nullable=False)
    bmi = Column(Float, nullable=False)
    diabetes_pedigree_function = Column(Float, nullable=False)

    probability = Column(Float, nullable=False)
    risk_level = Column(String, index=True, nullable=False)
    health_score = Column(Float, nullable=False)
    recommendation = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
