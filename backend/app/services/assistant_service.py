import requests
from app.core.config import OLLAMA_URL, OLLAMA_MODEL

SYSTEM_PROMPT = '''
You are GlucoVerse AI, a preventive healthcare assistant.
Explain diabetes risk reports in simple words.
Do not diagnose disease.
Do not prescribe medicine.
Do not claim certainty.
Always recommend consulting a qualified doctor for high-risk cases.
Keep answers short, practical, and safe.
'''

def ask_local_ollama(question: str, risk_level: str | None = None) -> str:
    risk_context = f"Current risk level: {risk_level}" if risk_level else "Risk level not provided."

    prompt = f'''
{SYSTEM_PROMPT}

{risk_context}

User question:
{question}

Answer:
'''

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response generated.")
    except requests.exceptions.ConnectionError:
        return (
            "Ollama is not running. Install Ollama, run `ollama pull llama3.2:3b`, "
            "then start Ollama and try again."
        )
    except requests.exceptions.Timeout:
        return "Ollama response timed out. Try using a smaller model."
    except Exception as exc:
        return f"Local assistant error: {str(exc)}"
