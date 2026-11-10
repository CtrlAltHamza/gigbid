import re
from typing import Any
from rag.ingest.loaders import DocumentChunk
from rag.index.vector_index import DenseVectorIndex

def extract_sub_requirements(job_text: str) -> list[str]:
    """Decomposes complex job post into atomic requirements."""
    # Split by sentences, bullet points, and commas
    lines = [line.strip() for line in job_text.replace(";", "\n").replace("•", "\n").replace("-", "\n").splitlines()]
    candidates = []
    for line in lines:
        if len(line) > 15:
            candidates.append(line)
    if not candidates:
        candidates = [job_text]
    return candidates[:4]

def retrieve(query: str, chunks: list[DocumentChunk], k: int = 5) -> list[dict[str, Any]]:
    """
    V1 Requirement Decomposition:
    Splits job post into multiple sub-requirements, retrieves top matches for each,
    and merges candidate items via Reciprocal Rank Fusion (RRF).
    """
    sub_queries = extract_sub_requirements(query)
    index = DenseVectorIndex(chunks)

    # RRF scoring dict: chunk_id -> rrf_score
    rrf_scores: dict[str, float] = {}
    chunk_map: dict[str, DocumentChunk] = {}
    k_rrf = 60.0

    for sub_q in sub_queries:
        sub_ranked = index.search(query=sub_q, k=k * 2)
        for rank, (chunk, score) in enumerate(sub_ranked):
            chunk_map[chunk.chunk_id] = chunk
            rrf_scores[chunk.chunk_id] = rrf_scores.get(chunk.chunk_id, 0.0) + (1.0 / (k_rrf + rank + 1))

    # Sort merged results by RRF score
    sorted_items = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:k]
    
    max_rrf = sorted_items[0][1] if sorted_items else 1.0
    return [
        {
            "chunk_id": cid,
            "score": round(score / max_rrf, 4),
            "text": chunk_map[cid].text[:300],
            "metadata": chunk_map[cid].metadata,
            "variant": "V1_Decomposition"
        }
        for cid, score in sorted_items
    ]
