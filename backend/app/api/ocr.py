import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.ocr_service import scan_report

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/ocr/extract")
async def extract_report(
    patient_name: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        print("OCR request received")
        print("Patient:", patient_name)
        print("File:", file.filename)

        if not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")

        allowed_extensions = [".png", ".jpg", ".jpeg"]
        ext = os.path.splitext(file.filename)[1].lower()

        if ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail="Only PNG, JPG, and JPEG files are supported"
            )

        safe_filename = file.filename.replace(" ", "_")
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        print("Saving file...")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("File saved:", file_path)
        print("Starting OCR...")

        result = scan_report(file_path)

        print("OCR finished")

        return {
            "patient_name": patient_name,
            "filename": file.filename,
            "extracted_values": result.get("extracted_values", {}),
            "extracted_text_preview": result.get("extracted_text", "")[:1200]
        }

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR timeout or runtime error: {str(e)}"
        )

    except HTTPException:
        raise

    except Exception as e:
        print("OCR error:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"OCR failed: {str(e)}"
        )
