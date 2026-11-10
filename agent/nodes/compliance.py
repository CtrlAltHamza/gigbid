import time
import datetime
import re
from typing import Any
from agent.state import GigBidState
from agent.handoffs import ComplianceVerdict

def compliance_node(state: GigBidState) -> dict[str, Any]:
    """Compliance Guard node: Validates draft against platform policies and strips prohibited items."""
    t0 = time.perf_counter()
    draft = state.get("proposal_draft", {})
    text = draft.get("cover_letter", "")
    
    violations = []
    sanitized = text

    # 1. Strip off-platform emails
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.search(email_pattern, sanitized):
        violations.append("Prohibited email address detected.")
        sanitized = re.sub(email_pattern, "[CONTACT REMOVED BY COMPLIANCE]", sanitized)

    # 2. Strip off-platform phone numbers
    phone_pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    if re.search(phone_pattern, sanitized):
        violations.append("Prohibited phone number detected.")
        sanitized = re.sub(phone_pattern, "[PHONE REMOVED BY COMPLIANCE]", sanitized)

    # 3. Strip off-platform messaging handles (Telegram / WhatsApp)
    social_pattern = r"(telegram|whatsapp|skype|wechat|signal)\s*[:@\s]\s*[\w\+]+"
    if re.search(social_pattern, sanitized, re.IGNORECASE):
        violations.append("Prohibited off-platform contact channel detected.")
        sanitized = re.sub(social_pattern, "[OFF-PLATFORM CHANNEL REMOVED]", sanitized, flags=re.IGNORECASE)

    # 4. Strip unrealistic guarantees
    guarantee_pattern = r"(100%\s+guarantee|guaranteed\s+success|double\s+your\s+revenue)"
    if re.search(guarantee_pattern, sanitized, re.IGNORECASE):
        violations.append("Prohibited outcome guarantee detected.")
        sanitized = re.sub(guarantee_pattern, "high-probability delivery", sanitized, flags=re.IGNORECASE)

    verdict = ComplianceVerdict(
        compliant=(len(violations) == 0),
        violations=violations,
        sanitized_draft=sanitized
    )

    # Update proposal draft with sanitized content
    updated_draft = dict(draft)
    updated_draft["cover_letter"] = sanitized

    trace_item = {
        "node": "compliance",
        "tool": None,
        "arguments": None,
        "observation": f"Compliance check: {'Passed' if verdict.compliant else f'{len(violations)} violations sanitized'}",
        "latency_ms": round((time.perf_counter() - t0) * 1000, 2),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    return {
        "compliance_verdict": verdict.model_dump(),
        "proposal_draft": updated_draft,
        "execution_trace": [trace_item],
        "step_count": 1
    }
