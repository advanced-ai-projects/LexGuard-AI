from fastapi import FastAPI
from api.core.settings import get_settings

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.ENV}

# Local-only debug endpoint (safe pattern)
@app.get("/_config")
def config_debug():
    if settings.ENV != "local":
        return {"detail": "Not available"}
    return {
        "app": settings.APP_NAME,
        "env": settings.ENV,
        "aws_region": settings.AWS_REGION,
        "opensearch_url": settings.opensearch_url,
        "opensearch_index": settings.OPENSEARCH_INDEX,
        "bedrock_model_id": settings.BEDROCK_MODEL_ID,
    }
