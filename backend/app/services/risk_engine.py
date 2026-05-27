def classify_risk(probability: float) -> str:
    if probability < 0.35:
        return "Low Risk"
    if probability < 0.70:
        return "Moderate Risk"
    return "High Risk"

def calculate_health_score(probability: float, glucose: float, bmi: float) -> float:
    # Score out of 100. Higher means better preventive health status.
    score = 100 - (probability * 70)

    if glucose >= 140:
        score -= 10
    elif glucose >= 110:
        score -= 5

    if bmi >= 30:
        score -= 10
    elif bmi >= 25:
        score -= 5

    return round(max(0, min(100, score)), 2)

def generate_recommendation(risk_level: str, glucose: float, bmi: float, blood_pressure: float) -> str:
    advice = []

    if glucose >= 140:
        advice.append("Your glucose value appears high. Please monitor sugar levels and consult a healthcare professional.")
    elif glucose >= 110:
        advice.append("Your glucose value is slightly elevated. Maintain diet control and regular activity.")

    if bmi >= 30:
        advice.append("Your BMI is in the obese range. Weight management can help reduce diabetes risk.")
    elif bmi >= 25:
        advice.append("Your BMI is above the normal range. Regular exercise and balanced food habits may help.")

    if blood_pressure >= 140:
        advice.append("Blood pressure appears high. Regular monitoring is recommended.")

    if risk_level == "Low Risk":
        advice.append("Overall risk appears low. Continue healthy habits and periodic checkups.")
    elif risk_level == "Moderate Risk":
        advice.append("Moderate risk detected. Focus on preventive lifestyle changes and medical guidance.")
    else:
        advice.append("High risk detected. This is not a diagnosis, but you should consult a qualified doctor soon.")

    return " ".join(advice)

def generate_assistant_note(risk_level: str) -> str:
    return (
        f"GlucoVerse detected {risk_level}. "
        "This result is for preventive screening only and is not a medical diagnosis."
    )
