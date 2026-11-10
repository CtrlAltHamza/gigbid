from typing import Any
from rag.ingest.loaders import DocumentChunk
from rag.variants.v2_hybrid import retrieve as hybrid_retrieve

def grade_evidence(query: str, evidence_items: list[dict[str, Any]], threshold: float = 0.50) -> dict[str, Any]:
    """
    Grades retrieved evidence against the job query.
    Returns sufficiency status and whether query expansion/re-query is needed.
    """
    if not evidence_items:
        return {"status": "none", "mean_score": 0.0, "is_sufficient": False}

    mean_score = sum(e["score"] for e in evidence_items) / len(evidence_items)
    is_sufficient = mean_score >= threshold

    return {
        "status": "sufficient" if is_sufficient else "weak",
        "mean_score": round(mean_score, 3),
        "is_sufficient": is_sufficient
    }

def expand_query(query: str) -> str:
    """Expands query with synonyms and technical variants."""
    expansions = {
        "classification": "classification logistic regression random forest precision recall",
        "churn": "churn prediction customer retention lifetime value cohort analysis",
        "rag": "RAG retrieval augmented generation vector search embeddings hallucination",
        "fastapi": "FastAPI REST API async backend microservice Uvicorn",
        "next.js": "Next.js React TypeScript frontend dashboard Tailwind",
        "dbt": "dbt SQL data models data warehouse Snowflake transform ETL",
    }
    expanded = query
    for key, syns in expansions.items():
        if key in query.lower():
            expanded += " " + syns
    return expanded

def retrieve(query: str, chunks: list[DocumentChunk], k: int = 5) -> list[dict[str, Any]]:
    """
    V8 Corrective Self-RAG Loop:
    1. Retrieve initial candidate evidence.
    2. Grade evidence sufficiency.
    3. If weak (< 0.50), expand query and re-retrieve.
    4. If still none, refuse to invent claims (flagged with can_bid=False).
    """
    initial_evidence = hybrid_retrieve(query, chunks, k=k)
    grade = grade_evidence(query, initial_evidence)

    if not grade["is_sufficient"]:
        # Re-query with expanded query
        expanded_q = expand_query(query)
        re_retrieved = hybrid_retrieve(expanded_q, chunks, k=k)
        re_grade = grade_evidence(expanded_q, re_retrieved)
        
        final_evidence = re_retrieved
        decision = "re-queried_sufficient" if re_grade["is_sufficient"] else "re-queried_weak"
    else:
        final_evidence = initial_evidence
        decision = "initial_sufficient"

    return [
        {
            **item,
            "corrective_decision": decision,
            "can_claim": grade["mean_score"] > 0.25,
            "variant": "V8_Corrective_Self_RAG"
        }
        for item in final_evidence
    ]

