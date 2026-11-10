import pytest
import uuid
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from agent.graphs.conversation_graph import build_conversation_graph

def test_conversation_graph_flow():
    checkpointer = MemorySaver()
    graph = build_conversation_graph(checkpointer=checkpointer)
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "thread_id": "thread-001",
        "client_id": "client-001",
        "freelancer_id": "ai_engineer",
        "messages": [
            {"sender_type": "client", "content": "Hi Alex, are you available for a 30-minute interview call this week?"}
        ]
    }

    # Stream until interrupt
    for _ in graph.stream(initial_state, config=config):
        pass

    state_snapshot = graph.get_state(config)
    assert state_snapshot.next == ("conversation_approval",)
    interrupt_val = state_snapshot.tasks[0].interrupts[0].value
    assert "suggested_reply" in interrupt_val

    # Resume with approval
    resumed = graph.invoke(Command(resume={"approved": True}), config=config)
    assert resumed["approval_status"] == "approved"
    assert "dispatched_message" in resumed
    assert resumed["dispatched_message"]["status"] == "sent"
