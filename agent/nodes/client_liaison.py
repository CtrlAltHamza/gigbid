import time
import datetime
from typing import Any
from agent.state import ConversationState
from mcp_servers.workspace.server import get_calendar_availability_tool

def client_liaison_node(state: ConversationState) -> dict[str, Any]:
    """Client Liaison node: Classifies message intent and drafts responses/calendar holds."""
    t0 = time.perf_counter()
    messages = state.get("messages", [])
    latest_msg = messages[-1] if messages else {"content": "Hi, are you free for a call?"}
    content_lower = latest_msg.get("content", "").lower()

    # Intent classification
    if "call" in content_lower or "interview" in content_lower or "sync" in content_lower or "meet" in content_lower:
        intent = "interview_request"
        slots = get_calendar_availability_tool(days_ahead=3)
        slot_text = ", ".join([s["start_time"][:16].replace("T", " ") + " UTC" for s in slots[:3]])
        reply = f"I would be glad to sync. Here are a few times I have available this week: {slot_text}. Please let me know which works best for you."
        proposed_slots = slots[:3]
    elif "discount" in content_lower or "rate" in content_lower or "price" in content_lower or "cheaper" in content_lower:
        intent = "negotiation"
        reply = "Thank you for discussing the scope. My quoted rate reflects production delivery with full test coverage and documentation. If budget is constrained, we can phase the deliverables starting with Phase 1 MVP."
        proposed_slots = []
    elif "telegram" in content_lower or "whatsapp" in content_lower or "outside" in content_lower or "free" in content_lower:
        intent = "scam_signal"
        reply = "To ensure mutual platform protection and adhere to marketplace terms, all communication and contracts must remain directly on the platform."
        proposed_slots = []
    else:
        intent = "question"
        reply = "Thank you for your question. Yes, I have direct experience handling this exact technical challenge and can implement it according to your specifications."
        proposed_slots = []

    trace_item = {
        "node": "client_liaison",
        "tool": "workspace.get_calendar_availability" if intent == "interview_request" else None,
        "arguments": None,
        "observation": f"Classified intent: '{intent}' -> Drafted response ({len(reply.split())} words)",
        "latency_ms": round((time.perf_counter() - t0) * 1000, 2),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    return {
        "detected_intent": intent,
        "suggested_reply": reply,
        "proposed_slots": proposed_slots,
        "approval_status": "pending_human_approval",
        "execution_trace": [trace_item]
    }
