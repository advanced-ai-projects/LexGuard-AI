from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Load from .env automatically
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignore unknown env vars
    )

    # App
    APP_NAME: str = "LexGuard AI"
    ENV: str = Field(default="local", description="local|dev|staging|prod")
    DEBUG: bool = True

    # AWS
    AWS_REGION: str = "eu-west-1"

    # OpenSearch (local or managed)
    OPENSEARCH_HOST: str = "localhost"
    OPENSEARCH_PORT: int = 9200
    OPENSEARCH_USE_SSL: bool = False
    OPENSEARCH_VERIFY_CERTS: bool = False
    OPENSEARCH_INDEX: str = "lexguard-docs"

    # Docs store (S3 later; local now still ok)
    S3_BUCKET: str = "lexguard-docs-bucket"

    # Bedrock (later)
    BEDROCK_MODEL_ID: str = "anthropic.claude-3-haiku-20240307-v1:0"

    @property
    def opensearch_url(self) -> str:
        scheme = "https" if self.OPENSEARCH_USE_SSL else "http"
        return f"{scheme}://{self.OPENSEARCH_HOST}:{self.OPENSEARCH_PORT}"


@lru_cache
def get_settings() -> Settings:
    # Cached singleton so settings isn't re-parsed on every request
    return Settings()
