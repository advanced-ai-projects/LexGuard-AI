import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict

from api.core.settings import get_settings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base: Dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        # attach extra fields if present
        extras = getattr(record, "extra", None)
        if isinstance(extras, dict):
            base.update(extras)

        if record.exc_info:
            base["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(base, ensure_ascii=False)


def setup_logging() -> None:
    """
    Configure root logging once.
    JSON logs are ideal for CloudWatch Insights + centralized logging.
    """
    settings = get_settings()
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    if settings.LOG_JSON:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        )

    root.addHandler(handler)

    # Reduce noisy loggers if desired
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
