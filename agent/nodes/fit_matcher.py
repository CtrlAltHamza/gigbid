import time
import datetime
from typing import Any
from agent.state import GigBidState
from agent.handoffs import FitReport
from rag.retriever import GigBidRetriever

def fit_matcher_node(state: GigBidState) -> dict[str, Any]:
    """Fit Matcher node: Maps JobSpec requirements to Portfolio MCP evidence."""
    t0 = time.perf_counter()
    job = state.get("job", {})
    persona_id = state.get("persona_id", "ai_engineer")
    
    query = f"{job.get('title', '')} {' '.join(job.get('required_skills', []))}"
    retriever = GigBidRetriever(persona_id=persona_id)
    evidence_items = retriever.retrieve_evidence(query=query, k=4)

    matched = []
    missing = []
    evidence_ids = []

    skills = job.get("required_skills", ["Python"])
    all_ev_text = " ".join([e.get("text", "").lower() for e in evidence_items])

    for s in skills:
        if s.lower() in all_ev_text:
            matched.append(s)
        else:
            missing.append(s)

    for e in evidence_items:
        evidence_ids.append(e.get("chunk_id") or e.get("evidence_id"))

    fit_score = len(matched) / max(1, len(skills))
    # Give baseline confidence if strong case study was matched
    if evidence_items and evidence_items[0].get("score", 0) > 0.4:
        fit_score = max(fit_score, 0.75)

    fit_report = FitReport(
        score=round(min(1.0, fit_score), 2),
        matched_skills=matched,
        missing_skills=missing,
        evidence_ids=evidence_ids,
        rationale=f"Matched {len(matched)}/{len(skills)} skills backed by {len(evidence_ids)} portfolio items."
    )

    trace_item = {
        "node": "fit_matcher",
        "tool": "portfolio.search_evidence",
        "arguments": {"requirement": query[:50], "k": 4},
        "observation": f"Fit score: {fit_report.score:.2f} ({len(matched)} matched, {len(missing)} missing)",
        "latency_ms": round((time.perf_counter() - t0) * 1000, 2),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    return {
        "fit_report": fit_report.model_dump(),
        "evidence": evidence_items,
        "execution_trace": [trace_item],
        "step_count": 1
    }
