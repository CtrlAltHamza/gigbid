import uuid
from typing import Any, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt

from agent.state import GigBidState
from agent.handoffs import BidDecision
from agent.nodes.scout import scout_node
from agent.nodes.analyst import analyst_node
from agent.nodes.risk_assessor import risk_assessor_node
from agent.nodes.fit_matcher import fit_matcher_node
from agent.nodes.pricing import pricing_node
from agent.nodes.writer import writer_node
from agent.nodes.verifier import verifier_node
from agent.nodes.critic import critic_node
from agent.nodes.compliance import compliance_node
from mcp_servers.marketplace.server import submit_proposal_tool
from agent.memory.promotion_rules import promote_user_edit_to_style_memory, promote_outcome_to_memory

def decision_node(state: GigBidState) -> dict[str, Any]:
    """Decision node: Evaluates risk and fit reports to decide skip vs watch vs bid."""
    risk = state.get("risk_report", {})
    fit = state.get("fit_report", {})
    
    risk_score = risk.get("score", 0.0)
    fit_score = fit.get("score", 0.0)
    is_scam = risk.get("is_scam", False)

    reasons = []
    if is_scam or risk_score >= 0.70:
        action = "skip"
        reasons.append(f"High risk score ({risk_score:.2f}): {risk.get('explanation')}")
    elif fit_score < 0.35:
        action = "skip"
        reasons.append(f"Insufficient portfolio skill fit ({fit_score:.2f})")
    elif fit_score < 0.60:
        action = "watch"
        reasons.append(f"Moderate fit ({fit_score:.2f}); candidate for review")
    else:
        action = "bid"
        reasons.append(f"Strong fit ({fit_score:.2f}) and acceptable risk profile ({risk_score:.2f})")

    decision = BidDecision(
        action=action,
        confidence=round(fit_score if action == "bid" else risk_score, 2),
        reasons=reasons
    )

    return {
        "decision": decision.model_dump(),
        "step_count": 1
    }

def route_decision(state: GigBidState) -> Literal["pricing", "__end__"]:
    dec = state.get("decision", {})
    if dec.get("action") == "skip":
        return "__end__"
    return "pricing"

def route_critic(state: GigBidState) -> Literal["writer", "compliance"]:
    critique = state.get("critique", {})
    revision_count = state.get("revision_count", 0)
    if not critique.get("passed", True) and revision_count < 2:
        return "writer"
    return "compliance"

def human_approval_node(state: GigBidState) -> dict[str, Any]:
    """
    Human Approval Gate:
    Uses native LangGraph interrupt() before spending Connects or submitting.
    Resumes with human approval decision, edit diffs, or rejection reason.
    """
    job = state.get("job", {})
    draft = state.get("proposal_draft", {})
    quote = state.get("price_quote", {})
    risk = state.get("risk_report", {})

    # Compute dry_run preview
    idempotency_key = f"dry-run-{draft.get('job_id', 'unknown')}-{uuid.uuid4().hex[:6]}"
    dry_run_preview = {
        "dry_run": True,
        "job_id": draft.get("job_id"),
        "bid_amount_usd": quote.get("recommended_bid_usd", 400.0),
        "connects_cost": quote.get("connects_cost", 6),
        "idempotency_key": idempotency_key
    }

    approval_payload = {
        "job_id": job.get("job_id"),
        "job_title": job.get("title"),
        "proposal_draft": draft,
        "evidence_items": state.get("evidence", []),
        "risk_report": risk,
        "price_quote": quote,
        "dry_run_preview": dry_run_preview,
        "instructions": "Approve, edit draft, or reject with reason."
    }

    # Pause execution until human resumes via UI
    user_response = interrupt(approval_payload)

    # Process human response
    approved = user_response.get("approved", True) if isinstance(user_response, dict) else True
    user_edits = user_response.get("user_edits") if isinstance(user_response, dict) else None
    rejection_reason = user_response.get("rejection_reason") if isinstance(user_response, dict) else None

    # Style memory promotion rule on user edits
    if user_edits and user_edits != draft.get("cover_letter"):
        promoted_rule = promote_user_edit_to_style_memory(draft.get("cover_letter", ""), user_edits)
        draft["cover_letter"] = user_edits

    return {
        "approval_status": "approved" if approved else "rejected",
        "proposal_draft": draft,
        "user_edits": user_edits,
        "rejection_reason": rejection_reason,
        "dry_run_preview": dry_run_preview,
        "step_count": 1
    }

def route_approval(state: GigBidState) -> Literal["marketplace_submit", "__end__"]:
    status = state.get("approval_status", "approved")
    if status == "approved":
        return "marketplace_submit"
    return "__end__"

def marketplace_submit_node(state: GigBidState) -> dict[str, Any]:
    """Submits approved proposal to Marketplace MCP using idempotency key."""
    draft = state.get("proposal_draft", {})
    quote = state.get("price_quote", {})
    idempotency_key = f"submit-{draft.get('job_id')}-{uuid.uuid4().hex[:8]}"

    result = submit_proposal_tool(
        job_id=draft.get("job_id"),
        bid_amount_usd=quote.get("recommended_bid_usd", 400.0),
        estimated_duration_days=14,
        cover_letter=draft.get("cover_letter", ""),
        screening_answers=draft.get("screening_answers", []),
        evidence_ids=draft.get("evidence_ids", []),
        idempotency_key=idempotency_key,
        dry_run=False
    )

    # Promote outcome to long-term memory
    category = state.get("job", {}).get("category", "machine-learning")
    promote_outcome_to_memory(category, result.get("status", "submitted"), draft.get("evidence_ids", []))

    return {
        "submission_result": result,
        "step_count": 1
    }

def build_bid_graph(checkpointer: Any | None = None):
    """Constructs the complete hand-written LangGraph StateGraph."""
    graph = StateGraph(GigBidState)

    # Register Nodes
    graph.add_node("scout", scout_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("risk_assessor", risk_assessor_node)
    graph.add_node("fit_matcher", fit_matcher_node)
    graph.add_node("decision_node", decision_node)
    graph.add_node("pricing", pricing_node)
    graph.add_node("writer", writer_node)
    graph.add_node("verifier", verifier_node)
    graph.add_node("critic", critic_node)
    graph.add_node("compliance", compliance_node)
    graph.add_node("human_approval", human_approval_node)
    graph.add_node("marketplace_submit", marketplace_submit_node)

    # Parallel Fan-Out: Scout -> [Analyst, Risk Assessor, Fit Matcher]
    graph.add_edge(START, "scout")
    graph.add_edge("scout", "analyst")
    graph.add_edge("scout", "risk_assessor")
    graph.add_edge("scout", "fit_matcher")

    # Fan-In: All three parallel branches merge into decision_node
    graph.add_edge("analyst", "decision_node")
    graph.add_edge("risk_assessor", "decision_node")
    graph.add_edge("fit_matcher", "decision_node")

    # Routing from decision
    graph.add_conditional_edges(
        "decision_node",
        route_decision,
        {"pricing": "pricing", "__end__": END}
    )

    # Sequential execution: Pricing -> Writer -> Verifier -> Critic
    graph.add_edge("pricing", "writer")
    graph.add_edge("writer", "verifier")
    graph.add_edge("verifier", "critic")

    # Bounded Critic Loop: Writer <-> Critic (max 2 revisions)
    graph.add_conditional_edges(
        "critic",
        route_critic,
        {"writer": "writer", "compliance": "compliance"}
    )

    # Compliance Guard -> Human Approval Gate -> Submit
    graph.add_edge("compliance", "human_approval")
    graph.add_conditional_edges(
        "human_approval",
        route_approval,
        {"marketplace_submit": "marketplace_submit", "__end__": END}
    )
    graph.add_edge("marketplace_submit", END)

    memory_checkpointer = checkpointer or MemorySaver()
    return graph.compile(checkpointer=memory_checkpointer)

# Default pre-compiled instance
bid_graph = build_bid_graph()
