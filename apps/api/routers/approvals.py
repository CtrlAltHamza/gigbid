from fastapi import APIRouter, HTTPException
from typing import Any
from langgraph.types import Command
from apps.api.schemas.models import ProposalActionRequest
from apps.api.streaming import api_bid_graph, active_threads

router = APIRouter(prefix="/api/approvals", tags=["approvals"])

@router.get("/pending")
def list_pending_approvals():
    """Lists all threads paused at human approval gate (persisted across page reloads)."""
    pending = []
    for thread_id, thread_info in active_threads.items():
        if thread_info.get("status") == "awaiting_approval":
            pending.append({
                "thread_id": thread_id,
                "job_id": thread_info.get("job_id"),
                "persona_id": thread_info.get("persona_id"),
                "payload": thread_info.get("interrupt_payload")
            })
    return pending

@router.post("/{thread_id}/resume")
def resume_approval(thread_id: str, action_req: ProposalActionRequest):
    """
    Resumes the interrupted LangGraph thread.
    - approve: submits proposal to marketplace
    - edit: diffs edits, saves to style memory, re-checks compliance, then submits
    - reject: archives thread with rejection reason
    """
    config = {"configurable": {"thread_id": thread_id}}
    state_snapshot = api_bid_graph.get_state(config)
    if not state_snapshot.next:
        raise HTTPException(status_code=400, detail="Thread is not in an interrupted state")

    resume_payload = {
        "approved": action_req.action in ["approve", "edit"],
        "user_edits": action_req.user_edits,
        "rejection_reason": action_req.rejection_reason
    }

    try:
        final_state = api_bid_graph.invoke(Command(resume=resume_payload), config=config)
        if thread_id in active_threads:
            active_threads[thread_id]["status"] = "completed"
            active_threads[thread_id]["final_state"] = final_state

        return {
            "status": "resumed_successfully",
            "thread_id": thread_id,
            "approval_status": final_state.get("approval_status"),
            "submission_result": final_state.get("submission_result")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resume thread: {str(e)}")

