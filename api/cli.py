import os
import sys


def run() -> None:
    """
    Run the FastAPI app with uvicorn.
    Usage: poetry run api
    """
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=port,
        reload=True,
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )


def test() -> None:
    """
    Run tests.
    Usage: poetry run test
    """
    import pytest

    raise SystemExit(pytest.main(["-q"]))
