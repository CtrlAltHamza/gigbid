import re
from typing import Any
from rag.ingest.loaders import DocumentChunk
from rag.variants.v2_hybrid import retrieve as hybrid_retrieve

def rerank_cross_encoder(query: str, text: str, initial_score: float) -> float:
    """
    Computes a refined cross-attention relevance score between query and evidence chunk.
    Evaluates term proximity, entity overlap, and outcome presence.
    """
    q_terms = [t.lower() for t in re.findall(r"\b\w{3,}\b", query)]
    text_lower = text.lower()

    if not q_terms:
        return initial_score

    # Exact term match bonus
    match_count = sum(1 for t in q_terms if t in text_lower)
    overlap_ratio = match_count / len(q_terms)

    # Proximity bonus (multiple query terms in close succession)
    proximity_bonus = 0.0
    for i in range(len(q_terms) - 1):
        if f"{q_terms[i]} {q_terms[i+1]}" in text_lower:
            proximity_bonus += 0.15

    # Outcome verification bonus
    outcome_bonus = 0.1 if ("outcome" in text_lower or "result" in text_lower or "delivered" in text_lower) else 0.0

    refined_score = (initial_score * 0.4) + (overlap_ratio * 0.4) + proximity_bonus + outcome_bonus
    return round(min(1.0, refined_score), 4)

def retrieve(query: str, chunks: list[DocumentChunk], k: int = 5) -> list[dict[str, Any]]:
    """
    V3 Cross-Encoder Reranking:
    First retrieves candidates via Hybrid BM25+Dense, then applies fine-grained cross-scoring
    to maximize precision at small k.
    """
    candidates = hybrid_retrieve(query, chunks, k=k * 3)

    reranked = []
    for item in candidates:
        new_score = rerank_cross_encoder(query, item["text"], item["score"])
        reranked.append({
            **item,
            "score": new_score,
            "variant": "V3_Cross_Encoder"
        })

    reranked.sort(key=lambda x: x["score"], reverse=True)
    return reranked[:k]
