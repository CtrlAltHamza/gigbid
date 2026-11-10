import os
import uuid
import datetime
from typing import Any
from mcp.server.fastmcp import FastMCP
from gigsim.engine import GigSimEngine
from gigsim.models import ProposalSubmission
from mcp_servers.marketplace.schemas import (
    SearchJobsInput, GetJobInput, GetClientHistoryInput, GetConnectsBalanceInput,
    CreateProposalDraftInput, SubmitProposalInput, SendMessageInput,
    ProposalResponse, MessageResponse
)
from mcp_servers.marketplace.audit import log_audit_event

# Initialize FastMCP Server
mcp = FastMCP("gigbid-marketplace-server")

# Shared backend engine (can connect to GigSim via in-process or HTTP)
engine = GigSimEngine()
idempotency_cache: dict[str, Any] = {}

# ----------------- READ TOOLS -----------------

@mcp.tool(
    name="search_jobs",
    description="Search active jobs in the marketplace with keywords, category, or budget filters. (Read-only)"
)
def search_jobs_tool(
    query: str = "",
    category: str | None = None,
    min_budget: float | None = None,
    max_budget: float | None = None,
    limit: int = 20
) -> list[dict[str, Any]]:
    jobs = engine.search_jobs(query=query, category=category, min_budget=min_budget, max_budget=max_budget, limit=limit)
    return [j.model_dump() for j in jobs]

@mcp.tool(
    name="get_job",
    description="Retrieve complete job details including screening questions, budget, and posted signals. (Read-only)"
)
def get_job_tool(job_id: str) -> dict[str, Any]:
    job = engine.get_job(job_id)
    if not job:
        raise ValueError(f"Job '{job_id}' not found")
    return job.model_dump()

@mcp.tool(
    name="get_client_history",
    description="Retrieve client hiring history, total spend, rating, and payment verification status. (Read-only)"
)
def get_client_history_tool(client_id: str) -> dict[str, Any]:
    client = engine.get_client(client_id)
    if not client:
        raise ValueError(f"Client '{client_id}' not found")
    data = client.model_dump()
    data.pop("hidden_preferences", None) # Do not leak hidden preferences to agents
    return data

@mcp.tool(
    name="get_connects_balance",
    description="Check the current Connects balance for the freelancer account. (Read-only)"
)
def get_connects_balance_tool(freelancer_id: str = "default") -> dict[str, Any]:
    balance = engine.get_connects_balance(freelancer_id)
    return {"freelancer_id": freelancer_id, "balance": balance}

@mcp.tool(
    name="list_messages",
    description="List conversation messages and client replies in a thread. (Read-only)"
)
def list_messages_tool(thread_id: str | None = None) -> list[dict[str, Any]]:
    msgs = engine.get_messages(thread_id)
    return [m.model_dump() for m in msgs]

# ----------------- WRITE TOOLS -----------------

@mcp.tool(
    name="create_proposal_draft",
    description="Create an internal proposal draft for a job before user review. Idempotent and non-destructive."
)
def create_proposal_draft_tool(
    job_id: str,
    bid_amount_usd: float,
    estimated_duration_days: int,
    cover_letter: str,
    idempotency_key: str,
    screening_answers: list[str] = [],
    evidence_ids: list[str] = [],
    freelancer_id: str = "default"
) -> dict[str, Any]:
    # Idempotency check
    if idempotency_key in idempotency_cache:
        return idempotency_cache[idempotency_key]

    job = engine.get_job(job_id)
    if not job:
        raise ValueError(f"Job '{job_id}' not found")

    draft = {
        "draft_id": f"draft-{uuid.uuid4().hex[:8]}",
        "job_id": job_id,
        "freelancer_id": freelancer_id,
        "bid_amount_usd": bid_amount_usd,
        "estimated_duration_days": estimated_duration_days,
        "cover_letter": cover_letter,
        "screening_answers": screening_answers,
        "evidence_ids": evidence_ids,
        "connects_required": job.connects_cost,
        "status": "pending_human_approval",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "idempotency_key": idempotency_key
    }
    
    idempotency_cache[idempotency_key] = draft
    log_audit_event(
        user=freelancer_id,
        tool="create_proposal_draft",
        arguments={"job_id": job_id, "bid": bid_amount_usd, "idempotency_key": idempotency_key},
        result=draft
    )
    return draft

@mcp.tool(
    name="submit_proposal",
    description="Submit an approved proposal to the marketplace. Destructive (spends Connects). Supports dry_run preview. Idempotent via idempotency_key."
)
def submit_proposal_tool(
    job_id: str,
    bid_amount_usd: float,
    estimated_duration_days: int,
    cover_letter: str,
    idempotency_key: str,
    dry_run: bool = False,
    screening_answers: list[str] = [],
    evidence_ids: list[str] = [],
    freelancer_id: str = "default"
) -> dict[str, Any]:
    # Check idempotency
    if idempotency_key in idempotency_cache and not dry_run:
        return idempotency_cache[idempotency_key]

    submission = ProposalSubmission(
        job_id=job_id,
        freelancer_id=freelancer_id,
        bid_amount_usd=bid_amount_usd,
        estimated_duration_days=estimated_duration_days,
        cover_letter=cover_letter,
        screening_answers=screening_answers,
        evidence_ids=evidence_ids,
        dry_run=dry_run,
        idempotency_key=idempotency_key
    )

    result = engine.submit_proposal(submission)
    
    if not dry_run:
        idempotency_cache[idempotency_key] = result
        log_audit_event(
            user=freelancer_id,
            tool="submit_proposal",
            arguments={"job_id": job_id, "bid": bid_amount_usd, "idempotency_key": idempotency_key, "dry_run": False},
            result=result
        )

    return result

@mcp.tool(
    name="send_message",
    description="Send a message or interview availability to a client thread. Destructive and idempotent."
)
def send_message_tool(
    thread_id: str,
    recipient_id: str,
    content: str,
    idempotency_key: str,
    sender_id: str = "default",
    dry_run: bool = False
) -> dict[str, Any]:
    if idempotency_key in idempotency_cache and not dry_run:
        return idempotency_cache[idempotency_key]

    if dry_run:
        return {
            "dry_run": True,
            "thread_id": thread_id,
            "recipient_id": recipient_id,
            "content_preview": content,
            "will_send": True
        }

    msg = engine.send_message(thread_id, sender_id, recipient_id, content)
    result = msg.model_dump()
    idempotency_cache[idempotency_key] = result

    log_audit_event(
        user=sender_id,
        tool="send_message",
        arguments={"thread_id": thread_id, "recipient": recipient_id, "idempotency_key": idempotency_key},
        result=result
    )
    return result

if __name__ == "__main__":
    mcp.run()
