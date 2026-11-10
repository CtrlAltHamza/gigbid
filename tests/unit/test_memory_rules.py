import pytest
from agent.memory.store import memory_store
from agent.memory.promotion_rules import promote_user_edit_to_style_memory, promote_outcome_to_memory

def test_style_memory_promotion_rule():
    original = "I am a passionate AI engineer excited to apply. I have done churn prediction [cs-ai-01]."
    edited = "I have done churn prediction [cs-ai-01] with 94% precision."

    promoted_rule = promote_user_edit_to_style_memory(original, edited)
    assert promoted_rule is not None
    assert "Always cut" in promoted_rule or "passionate" in promoted_rule

    rules = memory_store.get_style_rules()
    assert promoted_rule in rules

def test_outcome_memory_promotion_rule():
    success = promote_outcome_to_memory(
        category="machine-learning",
        outcome="won",
        evidence_ids=["cs-ai-01"]
    )
    assert success is True

    mem = memory_store.get_outcome_memory("machine-learning")
    assert mem["wins"] > 0
    assert "cs-ai-01" in mem["top_evidence"]

    # Raw intermediary status must not promote
    invalid = promote_outcome_to_memory(
        category="machine-learning",
        outcome="raw_tool_output",
        evidence_ids=[]
    )
    assert invalid is False

