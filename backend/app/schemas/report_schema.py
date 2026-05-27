from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class OCRExtractResponse(BaseModel):
    patient_name: str
    file_name: str
    extracted_values: Dict[str, float]
    extracted_text_preview: str

class ReportResponse(BaseModel):
    id: int
    patient_name: str
    file_name: str
    extracted_values_json: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
