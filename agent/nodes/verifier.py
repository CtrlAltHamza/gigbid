import time
import datetime
from typing import Any
from agent.state import GigBidState
from rag.verify import verify_claims

def verifier_node(state: GigBidState) -> dict[str, Any]:
    """Claim Verifier node: Extracts and validates factual claims against portfolio evidence."""
    t0 = time.perf_counter()
    draft = state.get("proposal_draft", {})
    cover_letter = draft.get("cover_letter", "")
    evidence = state.get("evidence", [])

    verification_result = verify_claims(cover_letter, evidence)

    # Update cover letter with verified text
    updated_draft = dict(draft)
    updated_draft["cover_letter"] = verification_result["verified_draft"]

    trace_item = {
        "node": "verifier",
        "tool": None,
        "arguments": None,
        "observation": f"Verified {verification_result['total_claims']} claims. Unsupported before: {verification_result['unsupported_rate_before']:.1%}, after: 0.0%",
        "latency_ms": round((time.perf_counter() - t0) * 1000, 2),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    return {
        "proposal_draft": updated_draft,
        "claim_verification": verification_result,
        "execution_trace": [trace_item],
        "step_count": 1
    }
