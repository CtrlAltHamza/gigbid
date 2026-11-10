from typing import Any
from rag.ingest.loaders import DocumentChunk
from rag.index.vector_index import DenseVectorIndex
from rag.index.bm25_index import BM25Index

def retrieve(query: str, chunks: list[DocumentChunk], k: int = 5, k_rrf: float = 60.0) -> list[dict[str, Any]]:
    """
    V2 Hybrid BM25 + Dense Cosine with Reciprocal Rank Fusion (RRF):
    Blends keyword-exact matches for specific tools/libraries with semantic embedding vectors.
    """
    vector_idx = DenseVectorIndex(chunks)
    bm25_idx = BM25Index(chunks)

    dense_ranked = vector_idx.search(query, k=k * 3)
    bm25_ranked = bm25_idx.search(query, k=k * 3)

    rrf_scores: dict[str, float] = {}
    chunk_map: dict[str, DocumentChunk] = {}

    # Accumulate Dense RRF
    for rank, (chunk, _) in enumerate(dense_ranked):
        chunk_map[chunk.chunk_id] = chunk
        rrf_scores[chunk.chunk_id] = rrf_scores.get(chunk.chunk_id, 0.0) + (1.0 / (k_rrf + rank + 1))

    # Accumulate BM25 RRF
    for rank, (chunk, _) in enumerate(bm25_ranked):
        chunk_map[chunk.chunk_id] = chunk
        rrf_scores[chunk.chunk_id] = rrf_scores.get(chunk.chunk_id, 0.0) + (1.0 / (k_rrf + rank + 1))

    sorted_items = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:k]
    max_score = sorted_items[0][1] if sorted_items else 1.0

    return [
        {
            "chunk_id": cid,
            "score": round(score / max_score, 4),
            "text": chunk_map[cid].text[:300],
            "metadata": chunk_map[cid].metadata,
            "variant": "V2_Hybrid_RRF"
        }
        for cid, score in sorted_items
    ]
