import joblib
import numpy as np
from app.core.config import MODEL_PATH, SCALER_PATH
from app.services.risk_engine import (
    classify_risk,
    calculate_health_score,
    generate_recommendation,
    generate_assistant_note
)

FEATURE_ORDER = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age"
]

_model = None
_scaler = None

def load_artifacts():
    global _model, _scaler

    if _model is None or _scaler is None:
        if not MODEL_PATH.exists() or not SCALER_PATH.exists():
            raise FileNotFoundError(
                "Model files not found. Run: python app/ml/train_model.py"
            )

        _model = joblib.load(MODEL_PATH)
        _scaler = joblib.load(SCALER_PATH)

    return _model, _scaler

def predict_diabetes_risk(payload):
    model, scaler = load_artifacts()

    features = np.array([[
        payload.pregnancies or 0,
        payload.glucose,
        payload.blood_pressure,
        payload.skin_thickness,
        payload.insulin,
        payload.bmi,
        payload.diabetes_pedigree_function,
        payload.age
    ]])

    scaled_features = scaler.transform(features)

    probability = float(model.predict_proba(scaled_features)[0][1])
    risk_level = classify_risk(probability)
    health_score = calculate_health_score(
        probability=probability,
        glucose=payload.glucose,
        bmi=payload.bmi
    )
    recommendation = generate_recommendation(
        risk_level=risk_level,
        glucose=payload.glucose,
        bmi=payload.bmi,
        blood_pressure=payload.blood_pressure
    )
    assistant_note = generate_assistant_note(risk_level)

    return {
        "probability": round(probability, 4),
        "risk_level": risk_level,
        "health_score": health_score,
        "recommendation": recommendation,
        "assistant_note": assistant_note
    }
