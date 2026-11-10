import re
from rank_bm25 import BM25Okapi
from rag.ingest.loaders import DocumentChunk

class BM25Index:
    """Keyword-exact BM25 retrieval index for precise technology and library matching."""
    def __init__(self, chunks: list[DocumentChunk]):
        self.chunks = chunks
        self.corpus_tokens = [self._tokenize(c.text) for c in self.chunks]
        self.bm25 = BM25Okapi(self.corpus_tokens)

    def _tokenize(self, text: str) -> list[str]:
        return [t.lower() for t in re.findall(r"\b[a-zA-Z0-9_\-\.\#\+]{2,}\b", text)]

    def search(self, query: str, k: int = 5) -> list[tuple[DocumentChunk, float]]:
        tokens = self._tokenize(query)
        if not tokens:
            return [(self.chunks[i], 0.0) for i in range(min(k, len(self.chunks)))]

        scores = self.bm25.get_scores(tokens)
        max_score = max(scores) if len(scores) > 0 and max(scores) > 0 else 1.0

        indexed_scores = [(self.chunks[i], round(float(scores[i] / max_score), 4)) for i in range(len(self.chunks))]
        indexed_scores.sort(key=lambda x: x[1], reverse=True)
        return indexed_scores[:k]

