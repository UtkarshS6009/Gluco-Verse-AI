# GlucoVerse AI Architecture

```text
Frontend
Next.js / Streamlit
        |
        v
FastAPI Local Backend
        |
        +--> Prediction API
        |       XGBoost model
        |       Scaler
        |       Risk engine
        |
        +--> OCR API
        |       OpenCV preprocessing
        |       Tesseract OCR
        |       Medical value extraction
        |
        +--> History API
        |       Patient timeline
        |       Previous reports
        |
        +--> Doctor API
        |       High-risk patients
        |       Patient summaries
        |
        +--> Admin API
        |       Risk distribution
        |       Health analytics
        |
        +--> Assistant API
                Local Ollama model
```

No external AI API key is required.
