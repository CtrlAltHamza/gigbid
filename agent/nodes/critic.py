import time
import datetime
from typing import Any
from agent.state import GigBidState
from agent.handoffs import Critique

def critic_node(state: GigBidState) -> dict[str, Any]:
    """Critic node: Evaluates grounding, personalization, length with bounded loops (<= 2)."""
    t0 = time.perf_counter()
    draft = state.get("proposal_draft", {})
    cover_letter = draft.get("cover_letter", "")
    ev_ids = draft.get("evidence_ids", [])
    revision_count = state.get("revision_count", 0)

    reasons = []
    score = 0.90

    # 1. Grounding check
    if not ev_ids:
        score -= 0.35
        reasons.append("Draft lacks explicit evidence citations.")

    # 2. Length check (ideal: 50-250 words)
    words = cover_letter.split()
    if len(words) > 250:
        score -= 0.15
        reasons.append(f"Proposal length ({len(words)} words) exceeds recommended 250 words limit.")
    elif len(words) < 30:
        score -= 0.20
        reasons.append("Proposal is too brief to convey engineering depth.")

    # 3. Generic opening check
    first_sentence = cover_letter.split(".")[0].lower() if cover_letter else ""
    if "passionate" in first_sentence or "writing to apply" in first_sentence:
        score -= 0.25
        reasons.append("Opening sentence contains boilerplate phrasing.")

    # Bounded Loop logic: If revisions >= 2, we must pass to avoid infinite loop
    max_revisions_reached = revision_count >= 2
    passed = (len(reasons) == 0) or max_revisions_reached

    critique = Critique(
        passed=passed,
        score=round(max(0.1, score), 2),
        revision_reasons=reasons,
        suggested_edits="Keep opening sentence strictly factual and reference concrete evidence IDs." if reasons else None
    )

    trace_item = {
        "node": "critic",
        "tool": "portfolio.get_case_study",
        "arguments": None,
        "observation": f"Critique score: {critique.score:.2f} (Passed: {critique.passed}, Revisions: {revision_count}/2)",
        "latency_ms": round((time.perf_counter() - t0) * 1000, 2),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    # Increment revision count only if failed and returning to writer
    next_revision_count = revision_count if passed else revision_count + 1

    return {
        "critique": critique.model_dump(),
        "revision_count": next_revision_count,
        "execution_trace": [trace_item],
        "step_count": 1
    }
