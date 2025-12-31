from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    APP_NAME: str = "LexGuard AI"
    ENV: str = Field(default="local", description="local|dev|staging|prod")
    DEBUG: bool = True

    # Logging
    LOG_LEVEL: str = "INFO"   # DEBUG|INFO|WARNING|ERROR
    LOG_JSON: bool = True

    # AWS
    AWS_REGION: str = "eu-west-1"

    # OpenSearch
    OPENSEARCH_HOST: str = "localhost"
    OPENSEARCH_PORT: int = 9200
    OPENSEARCH_USE_SSL: bool = False
    OPENSEARCH_VERIFY_CERTS: bool = False
    OPENSEARCH_INDEX: str = "lexguard-docs"

    OPENSEARCH_AUTH_MODE: str = "none"  # none|basic|sigv4
    OPENSEARCH_USERNAME: str | None = None
    OPENSEARCH_PASSWORD: str | None = None
    OPENSEARCH_AWS_SERVICE: str = "es"

    # Docs (S3 later)
    S3_BUCKET: str = "lexguard-docs-bucket"

    # Bedrock (safe toggle)
    BEDROCK_ENABLED: bool = False
    BEDROCK_REGION: str | None = None
    BEDROCK_MODEL_ID: str = "anthropic.claude-3-haiku-20240307-v1:0"
    BEDROCK_MAX_TOKENS: int = 512
    BEDROCK_TEMPERATURE: float = 0.2

    @property
    def opensearch_url(self) -> str:
        scheme = "https" if self.OPENSEARCH_USE_SSL else "http"
        return f"{scheme}://{self.OPENSEARCH_HOST}:{self.OPENSEARCH_PORT}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
