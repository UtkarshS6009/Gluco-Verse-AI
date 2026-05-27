from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.models.user import User
from app.models.prediction_record import PredictionRecord
from app.models.report import Report
from app.models.doctor_patient import DoctorPatient

from app.api.prediction import router as prediction_router
from app.api.history import router as history_router
from app.api.ocr import router as ocr_router
from app.api.doctor import router as doctor_router
from app.api.admin import router as admin_router
from app.api.assistant import router as assistant_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GlucoVerse AI Backend",
    description="Local-first AI preventive healthcare SaaS backend for diabetes risk prediction, OCR report scanning, history tracking, doctor panel, admin analytics, and Ollama assistant.",
    version="1.0.0"
)

# CORS must be added AFTER app = FastAPI(...)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router, prefix="/api", tags=["Prediction"])
app.include_router(history_router, prefix="/api", tags=["History"])
app.include_router(ocr_router, prefix="/api", tags=["OCR Report Scanning"])
app.include_router(doctor_router, prefix="/api", tags=["Doctor Panel"])
app.include_router(admin_router, prefix="/api", tags=["Admin Analytics"])
app.include_router(assistant_router, prefix="/api", tags=["Local AI Assistant"])


@app.get("/")
def root():
    return {
        "message": "GlucoVerse AI Backend is running",
        "external_ai_api_required": False,
        "local_ai": "Ollama optional",
        "docs": "/docs",
        "status": "healthy"
    }