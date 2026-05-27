from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class DoctorPatient(Base):
    __tablename__ = "doctor_patients"

    id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String, index=True, nullable=False)
    patient_name = Column(String, index=True, nullable=False)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
