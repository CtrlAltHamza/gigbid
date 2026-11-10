import uuid
from typing import Any, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt

from agent.state import ConversationState
from agent.nodes.client_liaison import client_liaison_node
from mcp_servers.marketplace.server import send_message_tool

def conversation_approval_node(state: ConversationState) -> dict[str, Any]:
    """Human approval gate for client messages."""
    thread_id = state.get("thread_id", "default")
    suggested_reply = state.get("suggested_reply", "")
    slots = state.get("proposed_slots", [])

    payload = {
        "thread_id": thread_id,
        "suggested_reply": suggested_reply,
        "proposed_slots": slots,
        "instructions": "Approve message or provide edited content."
    }

    user_response = interrupt(payload)
    approved = user_response.get("approved", True) if isinstance(user_response, dict) else True
    user_edits = user_response.get("user_edits") if isinstance(user_response, dict) else None

    final_reply = user_edits or suggested_reply

    return {
        "approval_status": "approved" if approved else "rejected",
        "suggested_reply": final_reply
    }

def route_conversation_approval(state: ConversationState) -> Literal["dispatch_message", "__end__"]:
    status = state.get("approval_status", "approved")
    if status == "approved":
        return "dispatch_message"
    return "__end__"

def dispatch_message_node(state: ConversationState) -> dict[str, Any]:
    """Dispatches client reply through Marketplace MCP."""
    thread_id = state.get("thread_id", "default")
    recipient_id = state.get("client_id", "client")
    content = state.get("suggested_reply", "")
    idempotency_key = f"msg-{thread_id}-{uuid.uuid4().hex[:8]}"

    res = send_message_tool(
        thread_id=thread_id,
        recipient_id=recipient_id,
        content=content,
        idempotency_key=idempotency_key,
        sender_id=state.get("freelancer_id", "default"),
        dry_run=False
    )

    dispatched = dict(res)
    dispatched["status"] = "sent"

    return {"dispatched_message": dispatched}

def build_conversation_graph(checkpointer: Any | None = None):
    """Constructs the Conversation Graph."""
    graph = StateGraph(ConversationState)

    graph.add_node("client_liaison", client_liaison_node)
    graph.add_node("conversation_approval", conversation_approval_node)
    graph.add_node("dispatch_message", dispatch_message_node)

    graph.add_edge(START, "client_liaison")
    graph.add_edge("client_liaison", "conversation_approval")
    graph.add_conditional_edges(
        "conversation_approval",
        route_conversation_approval,
        {"dispatch_message": "dispatch_message", "__end__": END}
    )
    graph.add_edge("dispatch_message", END)

    memory_checkpointer = checkpointer or MemorySaver()
    return graph.compile(checkpointer=memory_checkpointer)

conversation_graph = build_conversation_graph()
