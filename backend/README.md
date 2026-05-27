# GlucoVerse AI Backend

GlucoVerse AI is a local-first preventive healthcare backend for diabetes risk prediction, OCR-based medical report scanning, patient history tracking, doctor monitoring, admin analytics, and local AI health explanations using Ollama.

## Key rule

This project does not require OpenAI, Groq, Gemini, or any paid external AI API.

It uses:
- Local ML model using XGBoost
- Local FastAPI backend
- Local SQLite database
- Local OCR using OpenCV + Tesseract
- Optional local AI assistant using Ollama

## Folder Structure

```text
glucoverse_backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── prediction.py
│   │   ├── history.py
│   │   ├── ocr.py
│   │   ├── doctor.py
│   │   └── admin.py
│   ├── ml/
│   │   ├── train_model.py
│   │   ├── diabetes_model.pkl
│   │   ├── scaler.pkl
│   │   └── metrics.json
│   ├── services/
│   │   ├── prediction_service.py
│   │   ├── risk_engine.py
│   │   ├── ocr_service.py
│   │   ├── analytics_service.py
│   │   └── assistant_service.py
│   ├── models/
│   │   ├── user.py
│   │   ├── prediction_record.py
│   │   ├── report.py
│   │   └── doctor_patient.py
│   ├── schemas/
│   │   ├── prediction_schema.py
│   │   ├── user_schema.py
│   │   └── report_schema.py
│   ├── db/
│   │   └── database.py
│   └── core/
│       └── config.py
├── data/
│   └── diabetes.csv
├── requirements.txt
└── README.md
```

## Setup

```bash
cd glucoverse_backend_complete
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Train the model

```bash
python app/ml/train_model.py
```

This creates:

```text
app/ml/diabetes_model.pkl
app/ml/scaler.pkl
app/ml/metrics.json
```

## Run backend

```bash
uvicorn app.main:app --reload
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Optional Ollama setup

Install Ollama, then run:

```bash
ollama pull llama3.2:3b
ollama run llama3.2:3b
```

The assistant endpoint will use your local Ollama server.

## Main APIs

### Prediction

```http
POST /api/predict
```

### History

```http
GET /api/history
GET /api/history/{patient_name}
```

### OCR

```http
POST /api/ocr/extract
```

### Doctor panel

```http
GET /api/doctor/high-risk
GET /api/doctor/patient/{patient_name}
```

### Admin dashboard

```http
GET /api/admin/overview
GET /api/admin/risk-distribution
GET /api/admin/health-trends
```

## Medical safety

GlucoVerse AI is not a diagnosis system. It provides preventive risk screening and educational insights only. Always consult a qualified medical professional for diagnosis, treatment, or medication decisions.
