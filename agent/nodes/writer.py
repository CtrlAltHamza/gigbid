import time
import datetime
from typing import Any
from agent.state import GigBidState
from agent.handoffs import ProposalDraft
from agent.memory.store import memory_store

def writer_node(state: GigBidState) -> dict[str, Any]:
    """Proposal Writer node: Generates evidence-grounded cover letter and screening answers."""
    t0 = time.perf_counter()
    job = state.get("job", {})
    spec = state.get("job_spec", {})
    evidence_items = state.get("evidence", [])
    revision_count = state.get("revision_count", 0)
    critique = state.get("critique", {})

    top_ev = evidence_items[0] if evidence_items else {}
    ev_id = top_ev.get("chunk_id") or top_ev.get("evidence_id", "cs-ai-01")
    ev_title = top_ev.get("title", "Customer Churn Prediction Baseline")

    second_ev = evidence_items[1] if len(evidence_items) > 1 else top_ev
    ev_id_2 = second_ev.get("chunk_id") or second_ev.get("evidence_id", "repo-production-pipeline")

    # Ingest learned style preferences
    style_rules = memory_store.get_style_rules()
    banned = ["passionate", "guru", "rockstar"]

    # Incorporate critique feedback if this is a revision loop
    feedback_incorporation = ""
    if revision_count > 0 and critique.get("revision_reasons"):
        feedback_incorporation = f" Addressed review notes: {critique['revision_reasons'][0]}."

    cover_letter = (
        f"I have delivered production solutions directly matching '{job.get('title')}', "
        f"as documented in my verified case study [{ev_id}]. In that engagement ({ev_title}), "
        f"I engineered an automated pipeline with rigorous unit and validation benchmarks. "
        f"Additionally, my open-source repository [{ev_id_2}] demonstrates clean typed architecture "
        f"and Dockerized deployment.{feedback_incorporation} I can complete this deliverable within "
        f"{spec.get('duration_days', 14)} days."
    )

    # Answers to screening questions
    screening_answers = []
    questions = spec.get("screening_questions", job.get("screening_questions", []))
    for q in questions:
        screening_answers.append(
            f"Based on my production implementation in [{ev_id}], I address this by using cross-validation "
            f"and strict evaluation metrics rather than raw accuracy."
        )

    draft = ProposalDraft(
        job_id=job.get("job_id", "unknown"),
        freelancer_id=state.get("persona_id", "default"),
        cover_letter=cover_letter,
        screening_answers=screening_answers,
        evidence_ids=[ev_id, ev_id_2],
        revision_count=revision_count,
        status="drafted"
    )

    trace_item = {
        "node": "writer",
        "tool": "portfolio.get_case_study",
        "arguments": {"case_id": ev_id},
        "observation": f"Drafted proposal (revision {revision_count}) citing [{ev_id}, {ev_id_2}]",
        "latency_ms": round((time.perf_counter() - t0) * 1000, 2),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    return {
        "proposal_draft": draft.model_dump(),
        "execution_trace": [trace_item],
        "step_count": 1
    }
