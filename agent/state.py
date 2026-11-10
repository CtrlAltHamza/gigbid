import operator
from typing import Annotated, Any, TypedDict
from agent.handoffs import (
    JobSpec, RiskReport, FitReport, BidDecision, PriceQuote,
    ProposalDraft, Critique, ComplianceVerdict
)

class ExecutionTraceItem(TypedDict):
    node: str
    tool: str | None
    arguments: dict[str, Any] | None
    observation: Any
    latency_ms: float
    timestamp: str

class GigBidState(TypedDict, total=False):
    # 1. State: what this job run needs right now
    job: dict[str, Any]
    persona_id: str
    job_spec: dict[str, Any]
    risk_report: dict[str, Any]
    fit_report: dict[str, Any]
    decision: dict[str, Any]
    evidence: list[dict[str, Any]]
    price_quote: dict[str, Any]
    proposal_draft: dict[str, Any]
    claim_verification: dict[str, Any]
    critique: dict[str, Any]
    compliance_verdict: dict[str, Any]
    revision_count: int
    approval_status: str
    user_edits: str | None
    rejection_reason: str | None
    dry_run_preview: dict[str, Any]
    submission_result: dict[str, Any]
    
    # Reducers for parallel fan-in and tracing
    execution_trace: Annotated[list[dict[str, Any]], operator.add]
    errors: Annotated[list[str], operator.add]
    step_count: Annotated[int, operator.add]
    token_usage: Annotated[int, operator.add]

class ConversationState(TypedDict, total=False):
    thread_id: str
    client_id: str
    freelancer_id: str
    messages: list[dict[str, Any]]
    detected_intent: str
    suggested_reply: str
    proposed_slots: list[dict[str, Any]]
    approval_status: str
    dispatched_message: dict[str, Any]
    execution_trace: Annotated[list[dict[str, Any]], operator.add]
    errors: Annotated[list[str], operator.add]
