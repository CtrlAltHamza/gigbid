import os
import yaml
from typing import Any, Callable
from rag.ingest.loaders import DocumentChunk, load_persona_corpus
from rag.variants import (
    v0_naive,
    v1_decomposition,
    v2_hybrid,
    v3_cross_encoder,
    v4_outcome_aware,
    v8_corrective,
)

VARIANT_REGISTRY: dict[str, Callable[..., list[dict[str, Any]]]] = {
    "v0": v0_naive.retrieve,
    "v0_naive": v0_naive.retrieve,
    "v1": v1_decomposition.retrieve,
    "v1_decomposition": v1_decomposition.retrieve,
    "v2": v2_hybrid.retrieve,
    "v2_hybrid": v2_hybrid.retrieve,
    "v3": v3_cross_encoder.retrieve,
    "v3_cross_encoder": v3_cross_encoder.retrieve,
    "v4": v4_outcome_aware.retrieve,
    "v4_outcome_aware": v4_outcome_aware.retrieve,
    "v8": v8_corrective.retrieve,
    "v8_corrective": v8_corrective.retrieve,
}

def get_active_variant_name() -> str:
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "agent", "config.yaml"))
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f)
                return cfg.get("rag", {}).get("active_variant", "v2_hybrid")
        except Exception:
            pass
    return "v2_hybrid"

class GigBidRetriever:
    """Configurable Advanced RAG Retriever Factory."""
    def __init__(self, variant: str | None = None, persona_id: str = "ai_engineer"):
        self.variant_name = variant or get_active_variant_name()
        self.persona_id = persona_id
        self.chunks: list[DocumentChunk] = load_persona_corpus(persona_id)
        self.retrieve_fn = VARIANT_REGISTRY.get(self.variant_name.lower(), v2_hybrid.retrieve)

    def retrieve_evidence(self, query: str, k: int = 5) -> list[dict[str, Any]]:
        return self.retrieve_fn(query=query, chunks=self.chunks, k=k)

