import re
import cv2
import pytesseract
from pathlib import Path

def preprocess_image(image_path: str):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not read uploaded image.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.medianBlur(gray, 3)
    threshold = cv2.threshold(
        denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return threshold

def extract_text_from_image(image_path: str) -> str:
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image)
    return text

def extract_medical_values_from_text(text: str) -> dict:
    cleaned = text.lower().replace(":", " ").replace("=", " ")

    patterns = {
        "glucose": r"(glucose|blood sugar|fasting glucose|fbs)\D{0,30}(\d+(\.\d+)?)",
        "blood_pressure": r"(blood pressure|bp)\D{0,30}(\d{2,3})",
        "insulin": r"(insulin)\D{0,30}(\d+(\.\d+)?)",
        "bmi": r"(bmi|body mass index)\D{0,30}(\d+(\.\d+)?)",
        "hba1c": r"(hba1c|hb a1c|a1c)\D{0,30}(\d+(\.\d+)?)"
    }

    values = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, cleaned)
        if match:
            try:
                values[key] = float(match.group(2))
            except ValueError:
                pass

    return values

def process_report_image(image_path: str) -> dict:
    text = extract_text_from_image(image_path)
    values = extract_medical_values_from_text(text)

    return {
        "text": text,
        "values": values
    }
