# ---------- Builder ----------
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (keep minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry in builder only
ENV POETRY_VERSION=1.8.3
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Copy dependency files first (better layer caching)
COPY pyproject.toml poetry.lock* /app/

# Export requirements from Poetry (no need to install project package)
RUN poetry export -f requirements.txt --without-hashes -o /app/requirements.txt

# ---------- Runtime ----------
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime deps only
COPY --from=builder /app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app code
COPY api /app/api

# Expose port (ALB/ECS uses containerPort)
EXPOSE 8000

# Uvicorn command for ECS (no reload)
# Note: In ECS you typically set PORT=8000 or map it via task definition
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
