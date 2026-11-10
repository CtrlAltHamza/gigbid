import time
import datetime
from typing import Any
from agent.state import GigBidState

def scout_node(state: GigBidState) -> dict[str, Any]:
    """Scout node: Ingests and validates incoming job post."""
    t0 = time.perf_counter()
    job = state.get("job", {})
    if not job:
        raise ValueError("Scout node received empty job post")

    trace_item = {
        "node": "scout",
        "tool": "marketplace.get_job",
        "arguments": {"job_id": job.get("job_id")},
        "observation": f"Scouted job '{job.get('title')}' with connects cost {job.get('connects_cost', 6)}",
        "latency_ms": round((time.perf_counter() - t0) * 1000, 2),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    return {
        "execution_trace": [trace_item],
        "step_count": 1,
        "revision_count": 0
    }
