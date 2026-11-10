import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from mcp_servers.marketplace.server import get_job_tool
from apps.api.streaming import stream_job_analysis, active_threads, api_bid_graph

router = APIRouter(prefix="/api/runs", tags=["runs"])

@router.get("/stream/{job_id}")
async def stream_job_run(job_id: str, persona_id: str = "ai_engineer"):
    """Server-Sent Events endpoint streaming live LangGraph node-by-node execution."""
    job = get_job_tool(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    thread_id = f"thread-job-{job_id}-{uuid.uuid4().hex[:6]}"

    return StreamingResponse(
        stream_job_analysis(job=job, persona_id=persona_id, thread_id=thread_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Thread-ID": thread_id
        }
    )

@router.get("/{thread_id}")
def get_run_details(thread_id: str):
    info = active_threads.get(thread_id)
    config = {"configurable": {"thread_id": thread_id}}
    state = api_bid_graph.get_state(config)
    
    return {
        "thread_id": thread_id,
        "status": info.get("status") if info else "unknown",
        "state_values": state.values,
        "next_nodes": state.next,
        "trace": state.values.get("execution_trace", [])
    }

