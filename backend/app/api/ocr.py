import json
import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR
from app.db.database import get_db
from app.models.report import Report
from app.schemas.report_schema import OCRExtractResponse, ReportResponse
from app.services.ocr_service import process_report_image

router = APIRouter()

@router.post("/ocr/extract", response_model=OCRExtractResponse)
def extract_report_values(
    patient_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = process_report_image(str(file_path))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"OCR processing failed: {str(exc)}")

    report = Report(
        patient_name=patient_name,
        file_name=file.filename,
        extracted_text=result["text"],
        extracted_values_json=json.dumps(result["values"])
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return OCRExtractResponse(
        patient_name=patient_name,
        file_name=file.filename,
        extracted_values=result["values"],
        extracted_text_preview=result["text"][:500]
    )

@router.get("/ocr/reports", response_model=list[ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    return db.query(Report).order_by(Report.created_at.desc()).all()
