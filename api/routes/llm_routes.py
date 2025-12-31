from pydantic import BaseModel, Field
from fastapi import APIRouter

from api.clients.bedrock_client import generate_text
from api.core.settings import get_settings

router = APIRouter(prefix="/llm", tags=["llm"])


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=8000)


class GenerateResponse(BaseModel):
    model_id: str
    bedrock_enabled: bool
    text: str


@router.post("/generate", response_model=GenerateResponse)
def llm_generate(req: GenerateRequest):
    settings = get_settings()
    out = generate_text(req.prompt)

    return GenerateResponse(
        model_id=settings.BEDROCK_MODEL_ID,
        bedrock_enabled=settings.BEDROCK_ENABLED,
        text=out["text"],
    )
