from dataclasses import dataclass
from typing import Optional, List

@dataclass(frozen=True)
class RetrievalFilters:
    jurisdiction: Optional[str] = None   # e.g. "UK", "EU"
    domain: Optional[str] = None         # e.g. "employment", "tax"
    source: Optional[str] = None         # e.g. "GOV.UK", "ACAS"

def build_opensearch_filter(f: RetrievalFilters) -> List[dict]:
    must = []
    if f.jurisdiction:
        must.append({"term": {"jurisdiction.keyword": f.jurisdiction}})
    if f.domain:
        must.append({"term": {"domain.keyword": f.domain}})
    if f.source:
        must.append({"term": {"source.keyword": f.source}})
    return must
