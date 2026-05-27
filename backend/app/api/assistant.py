from fastapi import APIRouter
from app.schemas.user_schema import AssistantRequest, AssistantResponse
from app.services.assistant_service import ask_local_ollama

router = APIRouter()

@router.post("/assistant", response_model=AssistantResponse)
def assistant(payload: AssistantRequest):
    answer = ask_local_ollama(
        question=payload.question,
        risk_level=payload.risk_level
    )

    return AssistantResponse(
        answer=answer,
        source="Local Ollama"
    )
