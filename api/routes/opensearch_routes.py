from fastapi import APIRouter, Query
from api.clients.opensearch_client import get_opensearch_client
from api.core.settings import get_settings

router = APIRouter(prefix="/os", tags=["opensearch"])


@router.get("/ping")
def ping():
    client = get_opensearch_client()
    info = client.info()
    return {
        "ok": True,
        "cluster_name": info.get("cluster_name"),
        "version": info.get("version", {}).get("number"),
    }


@router.get("/search")
def search(q: str = Query(..., min_length=1), k: int = Query(5, ge=1, le=50)):
    """
    Minimal search stub.
    Assumes your documents have a 'content' field.
    """
    settings = get_settings()
    client = get_opensearch_client()

    body = {
        "size": k,
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["content^2", "title", "source"],
                "type": "best_fields",
            }
        },
    }

    res = client.search(index=settings.OPENSEARCH_INDEX, body=body)
    hits = res.get("hits", {}).get("hits", [])
    return {
        "query": q,
        "k": k,
        "count": len(hits),
        "results": [
            {
                "id": h.get("_id"),
                "score": h.get("_score"),
                "source": h.get("_source", {}),
            }
            for h in hits
        ],
    }
