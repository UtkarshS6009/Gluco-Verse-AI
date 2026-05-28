from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class AuthUser(Base):
    __tablename__ = "auth_users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="patient")
    created_at = Column(DateTime, default=datetime.utcnow)