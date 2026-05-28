import re
import cv2
import numpy as np
import pytesseract
from pathlib import Path

# Windows Tesseract path
# Change this path only if your tesseract.exe is installed somewhere else.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image_path: str):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not read uploaded image.")

    # Resize very large images to avoid OCR hanging
    height, width = image.shape[:2]

    max_width = 1200
    if width > max_width:
        scale = max_width / width
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = cv2.resize(image, (new_width, new_height))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    threshold = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    return threshold


    glucose = extract_number_near_label(
        text,
        ["glucose", "blood glucose", "fasting glucose", "random glucose", "sugar", "fbs"]
    )

    hba1c = extract_number_near_label(
        text,
        ["hba1c", "hb a1c", "glycated hemoglobin"]
    )

    bmi = extract_number_near_label(
        text,
        ["bmi", "body mass index"]
    )

    insulin = extract_number_near_label(
        text,
        ["insulin"]
    )

    blood_pressure = extract_number_near_label(
        text,
        ["blood pressure", "bp"]
    )

    if glucose is not None:
        values["glucose"] = glucose

    if hba1c is not None:
        values["hba1c"] = hba1c

    if bmi is not None:
        values["bmi"] = bmi

    if insulin is not None:
        values["insulin"] = insulin

    if blood_pressure is not None:
        values["blood_pressure"] = blood_pressure

    return values


def scan_report(image_path: str):
    processed_image = preprocess_image(image_path)

    # Timeout prevents infinite loading
    text = pytesseract.image_to_string(
        processed_image,
        config="--psm 6",
        timeout=20
    )

    extracted_values = extract_medical_values(text)

    return {
        "extracted_text": text,
        "extracted_values": extracted_values
