from __future__ import annotations

import json
from functools import lru_cache
from typing import Any, Dict

import boto3

from api.core.settings import get_settings


@lru_cache
def get_bedrock_runtime_client():
    """
    Cached boto3 Bedrock Runtime client.
    Will use default AWS credential resolution:
      - env vars
      - shared credentials (~/.aws/credentials)
      - SSO
      - instance/task role (ECS)
    """
    settings = get_settings()
    region = settings.BEDROCK_REGION or settings.AWS_REGION
    return boto3.client("bedrock-runtime", region_name=region)


def _anthropic_invoke(model_id: str, prompt: str, max_tokens: int, temperature: float) -> Dict[str, Any]:
    """
    Minimal Anthropic Claude request via Bedrock.
    Uses the Messages API style. Keep it small and safe.
    """
    brt = get_bedrock_runtime_client()

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ],
    }

    resp = brt.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json",
    )

    raw = resp["body"].read().decode("utf-8")
    data = json.loads(raw)

    # Claude responses typically look like: {"content":[{"type":"text","text":"..."}], ...}
    text = ""
    if isinstance(data.get("content"), list) and data["content"]:
        first = data["content"][0]
        if isinstance(first, dict):
            text = first.get("text", "")

    return {"text": text, "raw": data}


def generate_text(prompt: str) -> Dict[str, Any]:
    """
    Safe generator:
      - If BEDROCK_ENABLED is false => returns stub response (no costs).
      - If enabled => calls Bedrock.
    """
    settings = get_settings()

    if not settings.BEDROCK_ENABLED:
        return {
            "text": f"[STUBBED BEDROCK RESPONSE] You said: {prompt}",
            "raw": {"stub": True, "bedrock_enabled": False},
        }

    # For now: support Anthropic model ids. (We can add Titan / Llama later.)
    return _anthropic_invoke(
        model_id=settings.BEDROCK_MODEL_ID,
        prompt=prompt,
        max_tokens=settings.BEDROCK_MAX_TOKENS,
        temperature=settings.BEDROCK_TEMPERATURE,
    )
