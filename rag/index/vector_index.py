import math
import re
from typing import Any
from rag.ingest.loaders import DocumentChunk

class DenseVectorIndex:
    """
    In-memory dense vector index implementing normalized cosine similarity retrieval.
    Computes semantic term frequency-inverse document frequency embeddings.
    """
    def __init__(self, chunks: list[DocumentChunk]):
        self.chunks = chunks
        self.vocabulary: dict[str, int] = {}
        self.idf: dict[str, float] = {}
        self.doc_vectors: list[dict[int, float]] = []
        self._build_index()

    def _tokenize(self, text: str) -> list[str]:
        return [t.lower() for t in re.findall(r"\b[a-zA-Z0-9_\-\.\#\+]{2,}\b", text)]

    def _build_index(self):
        doc_count = len(self.chunks)
        df: dict[str, int] = {}

        # 1. Build vocab and document frequencies
        tokenized_docs = []
        for chunk in self.chunks:
            tokens = self._tokenize(chunk.text)
            tokenized_docs.append(tokens)
            unique_tokens = set(tokens)
            for t in unique_tokens:
                df[t] = df.get(t, 0) + 1
                if t not in self.vocabulary:
                    self.vocabulary[t] = len(self.vocabulary)

        # 2. Compute IDF
        for term, freq in df.items():
            self.idf[term] = math.log((doc_count + 1) / (freq + 1)) + 1.0

        # 3. Compute normalized TF-IDF vector per document
        for tokens in tokenized_docs:
            vec: dict[int, float] = {}
            for t in tokens:
                idx = self.vocabulary[t]
                vec[idx] = vec.get(idx, 0.0) + 1.0
            # TF log scaling and IDF weighting
            norm = 0.0
            for idx, count in vec.items():
                tfidf = (1.0 + math.log(count)) * self.idf[list(self.vocabulary.keys())[idx]]
                vec[idx] = tfidf
                norm += tfidf * tfidf
            norm = math.sqrt(norm) if norm > 0 else 1.0
            for idx in vec:
                vec[idx] /= norm
            self.doc_vectors.append(vec)

    def search(self, query: str, k: int = 5) -> list[tuple[DocumentChunk, float]]:
        """Compute cosine similarity between query vector and documents."""
        query_tokens = self._tokenize(query)
        q_vec: dict[int, float] = {}
        for t in query_tokens:
            if t in self.vocabulary:
                idx = self.vocabulary[t]
                q_vec[idx] = q_vec.get(idx, 0.0) + 1.0

        if not q_vec:
            return [(self.chunks[i], 0.0) for i in range(min(k, len(self.chunks)))]

        norm = 0.0
        for idx, count in q_vec.items():
            tfidf = (1.0 + math.log(count)) * self.idf[list(self.vocabulary.keys())[idx]]
            q_vec[idx] = tfidf
            norm += tfidf * tfidf
        norm = math.sqrt(norm) if norm > 0 else 1.0
        for idx in q_vec:
            q_vec[idx] /= norm

        scores = []
        for i, doc_vec in enumerate(self.doc_vectors):
            dot = sum(q_vec[idx] * doc_vec[idx] for idx in q_vec if idx in doc_vec)
            scores.append((self.chunks[i], round(dot, 4)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]

