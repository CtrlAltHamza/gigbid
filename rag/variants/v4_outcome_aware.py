from typing import Any
from rag.ingest.loaders import DocumentChunk
from rag.variants.v2_hybrid import retrieve as hybrid_retrieve

def retrieve(query: str, chunks: list[DocumentChunk], k: int = 5) -> list[dict[str, Any]]:
    """
    V4 Outcome-Aware Ranking:
    Retrieves candidate evidence chunks and applies positive outcome multipliers:
    - 1.35x for won proposals or 5.0 rated case studies
    - 1.15x for replied proposals
    - 0.85x for ignored proposals
    """
    candidates = hybrid_retrieve(query, chunks, k=k * 3)

    scored = []
    for item in candidates:
        meta = item.get("metadata", {})
        outcome = meta.get("outcome", "").lower()
        score = item["score"]

        multiplier = 1.0
        if "won" in outcome or "5.0" in outcome or "verified" in outcome:
            multiplier = 1.35
        elif "replied" in outcome or "interview" in outcome:
            multiplier = 1.15
        elif "ignored" in outcome or "rejected" in outcome:
            multiplier = 0.85

        adjusted_score = round(min(1.0, score * multiplier), 4)
        scored.append({
            **item,
            "score": adjusted_score,
            "outcome_multiplier": multiplier,
            "variant": "V4_Outcome_Aware"
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:k]
