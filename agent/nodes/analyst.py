import time
import datetime
from typing import Any
from agent.state import GigBidState
from agent.handoffs import JobSpec

def analyst_node(state: GigBidState) -> dict[str, Any]:
    """Job Analyst node: Extracts structured JobSpec from raw job text."""
    t0 = time.perf_counter()
    job = state.get("job", {})
    title = job.get("title", "")
    desc = job.get("description", "")
    budget_dict = job.get("budget", {})

    # Extract required skills and deliverables
    skills = job.get("required_skills", [])
    if not skills:
        for s in ["Python", "React", "TypeScript", "FastAPI", "SQL", "Docker", "scikit-learn"]:
            if s.lower() in desc.lower():
                skills.append(s)

    deliverables = [
        f"Deliver core implementation for {title}",
        "Provide test coverage and setup documentation"
    ]

    job_spec = JobSpec(
        job_id=job.get("job_id", "unknown"),
        title=title,
        deliverables=deliverables,
        required_skills=skills,
        budget_min=budget_dict.get("min", 200.0),
        budget_max=budget_dict.get("max", 500.0),
        duration_days=job.get("duration_days", 14),
        screening_questions=job.get("screening_questions", []),
        hidden_needs=["Clean async code", "Reproducible testing"],
        connects_cost=job.get("connects_cost", 6)
    )

    trace_item = {
        "node": "analyst",
        "tool": None,
        "arguments": None,
        "observation": f"Extracted JobSpec with {len(skills)} skills and budget ${job_spec.budget_min}-${job_spec.budget_max}",
        "latency_ms": round((time.perf_counter() - t0) * 1000, 2),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    return {
        "job_spec": job_spec.model_dump(),
        "execution_trace": [trace_item],
        "step_count": 1
    }
