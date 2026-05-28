import requests
from app.core.config import OLLAMA_URL, OLLAMA_MODEL

SYSTEM_PROMPT = """
You are GlucoVerse AI, a preventive healthcare education assistant.

Your job:
- Explain diabetes risk predictions in simple words.
- Explain glucose, BMI, insulin, blood pressure, and HbA1c values.
- Give general preventive lifestyle suggestions.
- Explain when a user should consult a doctor.

Rules:
- Do not diagnose disease.
- Do not prescribe medicines.
- Do not say "I cannot provide medical advice" as the main answer.
- Instead say: "This is not a diagnosis, but here is what the result may indicate."
- Keep the answer helpful, simple, and practical.
- Always recommend consulting a qualified healthcare professional for high-risk or serious symptoms.
"""

def ask_local_ollama(question: str, risk_level: str | None = None) -> str:
    prompt = f"""
{SYSTEM_PROMPT}

Current risk level:
{risk_level or "Not provided"}

User question:
{question}

Answer format:
1. Simple explanation
2. What it may indicate
3. Preventive suggestions
4. When to consult a doctor

Answer:
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)

        if response.status_code == 404:
            return (
                f"Ollama model not found. Run: ollama pull {OLLAMA_MODEL}"
            )

        response.raise_for_status()
        data = response.json()

        answer = data.get("response", "No response generated.")

        return answer.strip()

    except requests.exceptions.ConnectionError:
        return (
            "Ollama is not running. Open terminal and run: ollama serve. "
            "Then run: ollama pull llama3.2:3b"
        )

    except Exception as exc:
        return f"Local assistant error: {str(exc)}"