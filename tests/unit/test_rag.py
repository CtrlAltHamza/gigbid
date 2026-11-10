import pytest
from rag.ingest.loaders import load_persona_corpus, reindex_incremental
from rag.retriever import GigBidRetriever
from rag.verify import split_into_claims, check_claim_support, verify_claims

def test_ingestion_corpus_load():
    chunks = load_persona_corpus("ai_engineer")
    assert len(chunks) >= 50
    types = {c.metadata["type"] for c in chunks}
    assert "case_study" in types
    assert "cv" in types
    assert "past_proposal" in types
    assert "client_review" in types

def test_rag_variants_execution():
    retriever_v0 = GigBidRetriever(variant="v0_naive", persona_id="ai_engineer")
    res_v0 = retriever_v0.retrieve_evidence("customer churn prediction", k=3)
    assert len(res_v0) == 3

    retriever_v2 = GigBidRetriever(variant="v2_hybrid", persona_id="ai_engineer")
    res_v2 = retriever_v2.retrieve_evidence("customer churn prediction", k=3)
    assert len(res_v2) == 3

    retriever_v8 = GigBidRetriever(variant="v8_corrective", persona_id="ai_engineer")
    res_v8 = retriever_v8.retrieve_evidence("customer churn prediction", k=3)
    assert len(res_v8) == 3
    assert "corrective_decision" in res_v8[0]

def test_claim_verification_filtering():
    retriever = GigBidRetriever(variant="v2_hybrid", persona_id="ai_engineer")
    evidence = retriever.retrieve_evidence("scikit-learn classification", k=3)

    # Draft with 1 supported claim and 1 ungrounded hallucinated claim
    draft = "In my past project CS-AI-01, I built a customer churn model using scikit-learn. I also won an Olympic gold medal in rocket engineering."
    result = verify_claims(draft, evidence)

    assert result["total_claims"] == 2
    assert result["unsupported_count"] >= 1
    assert result["unsupported_rate_before"] > 0.0
    assert result["unsupported_rate_after"] == 0.0
    assert "Olympic gold medal" not in result["verified_draft"]

def test_incremental_reindexing():
    new_item = {
        "id": "new-case-study-99",
        "title": "Autonomous Agentic RAG Optimization",
        "text": "Engineered real-time LangGraph multi-agent RAG system with sub-100ms latency.",
        "skills": ["LangGraph", "Python"]
    }
    chunk = reindex_incremental(new_item, persona_id="ai_engineer")
    assert chunk.chunk_id == "new-case-study-99"

