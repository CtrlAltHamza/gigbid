from fastapi import APIRouter, HTTPException
from typing import Any
from mcp_servers.marketplace.server import engine
from apps.api.schemas.models import MessageActionRequest

router = APIRouter(prefix="/api/messages", tags=["messages"])

@router.get("")
def get_message_threads(thread_id: str | None = None):
    msgs = engine.get_messages(thread_id)
    return [m.model_dump() for m in msgs]

@router.post("/{thread_id}/reply")
def reply_to_thread(thread_id: str, req: MessageActionRequest):
    if req.action == "reject":
        return {"status": "rejected", "thread_id": thread_id}
    
    msg = engine.send_message(
        thread_id=thread_id,
        sender_id="freelancer",
        recipient_id="client",
        content=req.edited_reply or "Thank you for reaching out. I look forward to working together."
    )
    return {"status": "sent", "message": msg.model_dump()}

