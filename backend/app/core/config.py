from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

APP_NAME = "GlucoVerse AI"
APP_VERSION = "1.0.0"

DATABASE_URL = "sqlite:///./glucoverse.db"

MODEL_PATH = BASE_DIR / "app" / "ml" / "diabetes_model.pkl"
SCALER_PATH = BASE_DIR / "app" / "ml" / "scaler.pkl"
METRICS_PATH = BASE_DIR / "app" / "ml" / "metrics.json"
DATA_PATH = BASE_DIR / "data" / "diabetes.csv"

UPLOAD_DIR = BASE_DIR / "uploads" / "reports"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"
