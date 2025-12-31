from fastapi import FastAPI
from api.core.settings import get_settings

from api.routes.opensearch_routes import router as os_router
from api.routes.llm_routes import router as llm_router

from api.core.logging import setup_logging
from api.middleware.request_context import RequestLoggingMiddleware

setup_logging()

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, version="0.1.0")
app.add_middleware(RequestLoggingMiddleware)


app.include_router(os_router)
app.include_router(llm_router)


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.ENV}


@app.get("/_routes")
def list_routes():
    return sorted([r.path for r in app.routes])
