from typing import Any
from rag.ingest.loaders import DocumentChunk
from rag.index.vector_index import DenseVectorIndex

def retrieve(query: str, chunks: list[DocumentChunk], k: int = 5) -> list[dict[str, Any]]:
    """
    V0 Naive Dense Baseline:
    Takes the whole job post and runs top-k cosine similarity on fixed chunks.
    This is the baseline number that all advanced variants must beat.
    """
    index = DenseVectorIndex(chunks)
    ranked = index.search(query=query, k=k)
    return [
        {
            "chunk_id": chunk.chunk_id,
            "score": score,
            "text": chunk.text[:300],
            "metadata": chunk.metadata,
            "variant": "V0_Naive"
        }
        for chunk, score in ranked
    ]
