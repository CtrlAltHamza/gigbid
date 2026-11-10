import json
import asyncio
from typing import AsyncGenerator, Any
from agent.graphs.bid_graph import build_bid_graph
from langgraph.checkpoint.memory import MemorySaver

# Persistent thread checkpointer for API server
api_checkpointer = MemorySaver()
api_bid_graph = build_bid_graph(checkpointer=api_checkpointer)

# In-memory thread registry so approvals and page reloads never lose pending state
active_threads: dict[str, dict[str, Any]] = {}

async def stream_job_analysis(job: dict[str, Any], persona_id: str, thread_id: str) -> AsyncGenerator[str, None]:
    """
    Streams LangGraph multi-agent execution events to UI over Server-Sent Events (SSE).
    User never stares at a blank spinner during multi-second runs.
    """
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {
        "job": job,
        "persona_id": persona_id
    }

    active_threads[thread_id] = {
        "job_id": job.get("job_id"),
        "persona_id": persona_id,
        "status": "running",
        "state": initial_state
    }

    try:
        # Stream chunks from graph execution
        for chunk in api_bid_graph.stream(initial_state, config=config, stream_mode="updates"):
            for node_name, node_update in chunk.items():
                event_data = {
                    "node": node_name,
                    "update": node_update,
                    "thread_id": thread_id
                }
                yield f"event: node_update\ndata: {json.dumps(event_data)}\n\n"
                await asyncio.sleep(0.05) # Yield to event loop

        # Check if graph halted at interrupt
        state_snapshot = api_bid_graph.get_state(config)
        if state_snapshot.next and "human_approval" in state_snapshot.next:
            interrupt_payload = state_snapshot.tasks[0].interrupts[0].value if state_snapshot.tasks else {}
            active_threads[thread_id]["status"] = "awaiting_approval"
            active_threads[thread_id]["interrupt_payload"] = interrupt_payload
            yield f"event: interrupt\ndata: {json.dumps({'thread_id': thread_id, 'payload': interrupt_payload})}\n\n"
        else:
            active_threads[thread_id]["status"] = "completed"
            active_threads[thread_id]["result"] = state_snapshot.values
            yield f"event: complete\ndata: {json.dumps({'thread_id': thread_id, 'result': state_snapshot.values})}\n\n"

    except Exception as e:
        active_threads[thread_id]["status"] = "error"
        yield f"event: error\ndata: {json.dumps({'thread_id': thread_id, 'error': str(e)})}\n\n"
