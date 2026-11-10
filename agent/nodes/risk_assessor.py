import time
import datetime
import re
from typing import Any
from agent.state import GigBidState
from agent.handoffs import RiskReport

def risk_assessor_node(state: GigBidState) -> dict[str, Any]:
    """Risk Assessor node: Scores client risk, scam patterns, and prompt injections."""
    t0 = time.perf_counter()
    job = state.get("job", {})
    desc = job.get("description", "").lower()
    signals = job.get("warning_signals", [])
    
    score = 0.1
    flags = []
    is_scam = False
    has_injection = False

    # 1. Check prompt injection
    injection_patterns = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"system\s+(directive|override|notice)",
        r"bid\s+\$5",
        r"disregard\s+policy",
        r"system\s+compromised"
    ]
    for p in injection_patterns:
        if re.search(p, desc):
            score = 0.95
            flags.append("prompt_injection_detected")
            has_injection = True
            is_scam = True
            break

    # 2. Check unpaid trials
    if "unpaid_work" in signals or "for free" in desc or "unpaid trial" in desc or "free test" in desc:
        score = max(score, 0.90)
        flags.append("unpaid_work_request")
        is_scam = True

    # 3. Check off-platform contact
    if "off_platform_contact" in signals or "telegram" in desc or "whatsapp" in desc or "@" in desc:
        score = max(score, 0.85)
        flags.append("off_platform_contact_request")
        is_scam = True

    # 4. Check budget ceiling
    budget = job.get("budget", {})
    if budget.get("max", 100) == 0:
        score = max(score, 0.90)
        flags.append("zero_budget")

    if not flags:
        explanation = "Client has clean hiring profile with verified payment and realistic budget."
    else:
        explanation = f"Flagged high-risk attributes: {', '.join(flags)}."

    risk_report = RiskReport(
        score=min(1.0, score),
        flags=flags,
        explanation=explanation,
        is_scam=is_scam,
        has_injection=has_injection
    )

    trace_item = {
        "node": "risk_assessor",
        "tool": "marketplace.get_client_history",
        "arguments": {"client_id": job.get("client_id")},
        "observation": f"Risk score: {risk_report.score:.2f} (Flags: {len(flags)})",
        "latency_ms": round((time.perf_counter() - t0) * 1000, 2),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    return {
        "risk_report": risk_report.model_dump(),
        "execution_trace": [trace_item],
        "step_count": 1
    }
