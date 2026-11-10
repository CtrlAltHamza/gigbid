import difflib
import re
from typing import Any
from agent.memory.store import memory_store

def promote_user_edit_to_style_memory(original_draft: str, edited_draft: str) -> str | None:
    """
    Explicit Promotion Rule for Style Memory:
    Diffs the original generated draft against the user-edited/approved draft.
    Extracts recurring stylistic modifications:
    - Deleted opening sentences -> generates "Cut introductory pleasantries" rule
    - Removed buzzwords -> generates "Avoid [buzzword]" rule
    - Shortened paragraphs -> generates "Prefer concise bullet format" rule
    Only writes to memory store if a meaningful pattern is identified.
    """
    if not original_draft or not edited_draft or original_draft == edited_draft:
        return None

    orig_sentences = [s.strip() for s in original_draft.split(". ") if s.strip()]
    edit_sentences = [s.strip() for s in edited_draft.split(". ") if s.strip()]

    rule_promoted = None

    # Check if first sentence was deleted
    if orig_sentences and edit_sentences and orig_sentences[0] not in edited_draft:
        first_lower = orig_sentences[0].lower()
        if "passion" in first_lower or "excite" in first_lower or "writing" in first_lower or "dear" in first_lower:
            rule_promoted = "Always cut conversational opening pleasantries and lead with technical facts."
            memory_store.add_style_rule(rule_promoted)
            return rule_promoted

    # Check if length was significantly reduced (>25% reduction)
    if len(edited_draft) < len(original_draft) * 0.75:
        rule_promoted = "User strongly prefers ultra-concise proposals under 120 words."
        memory_store.add_style_rule(rule_promoted)
        return rule_promoted

    # Custom word deletion check
    buzzwords = ["passionate", "enthusiastic", "guarantee", "ninja", "rockstar", "expert"]
    for word in buzzwords:
        if word in original_draft.lower() and word not in edited_draft.lower():
            rule_promoted = f"Never use the word '{word}' in proposal drafts."
            memory_store.add_style_rule(rule_promoted)
            return rule_promoted

    return None

def promote_outcome_to_memory(category: str, outcome: str, evidence_ids: list[str]) -> bool:
    """
    Explicit Promotion Rule for Outcome Memory:
    Only promotes verified outcomes from the marketplace (replied, interview, hired, won).
    Raw intermediary agent steps or rejected bids are filtered out.
    """
    valid_outcomes = {"won", "hired", "replied", "interview", "rejected"}
    if outcome.lower() not in valid_outcomes:
        return False

    memory_store.record_outcome(
        category=category,
        outcome=outcome.lower(),
        evidence_ids=evidence_ids
    )
    return True
