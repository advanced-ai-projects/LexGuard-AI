from functools import lru_cache
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection

try:
    # Available in most opensearch-py 2.x builds
    from opensearchpy import AWSV4SignerAuth
except Exception:  # pragma: no cover
    AWSV4SignerAuth = None  # type: ignore

from api.core.settings import get_settings


@lru_cache
def get_opensearch_client() -> OpenSearch:
    """
    Returns a cached OpenSearch client.

    Supports:
      - local / self-managed: OPENSEARCH_AUTH_MODE=none|basic
      - AWS managed OpenSearch: OPENSEARCH_AUTH_MODE=sigv4
    """
    settings = get_settings()

    auth = None
    use_ssl = settings.OPENSEARCH_USE_SSL
    verify_certs = settings.OPENSEARCH_VERIFY_CERTS

    if settings.OPENSEARCH_AUTH_MODE == "basic":
        if not settings.OPENSEARCH_USERNAME or not settings.OPENSEARCH_PASSWORD:
            raise ValueError("Basic auth selected but OPENSEARCH_USERNAME/PASSWORD not set.")
        auth = (settings.OPENSEARCH_USERNAME, settings.OPENSEARCH_PASSWORD)

    elif settings.OPENSEARCH_AUTH_MODE == "sigv4":
        if AWSV4SignerAuth is None:
            raise RuntimeError(
                "AWSV4SignerAuth not available in your opensearch-py install. "
                "Upgrade opensearch-py or tell me your version and I'll align it."
            )

        session = boto3.Session(region_name=settings.AWS_REGION)
        creds = session.get_credentials()
        if creds is None:
            raise RuntimeError("No AWS credentials found for SigV4 auth (check AWS_PROFILE/ENV/SSO).")

        frozen = creds.get_frozen_credentials()
        auth = AWSV4SignerAuth(frozen, settings.AWS_REGION, settings.OPENSEARCH_AWS_SERVICE)

        # AWS managed OpenSearch uses SSL by default
        use_ssl = True if settings.OPENSEARCH_USE_SSL is False else settings.OPENSEARCH_USE_SSL

    client = OpenSearch(
        hosts=[{"host": settings.OPENSEARCH_HOST, "port": settings.OPENSEARCH_PORT}],
        http_auth=auth,
        use_ssl=use_ssl,
        verify_certs=verify_certs,
        connection_class=RequestsHttpConnection,
        timeout=30,
        max_retries=3,
        retry_on_timeout=True,
    )
    return client
