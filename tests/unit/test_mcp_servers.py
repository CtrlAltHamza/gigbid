import pytest
import uuid
from mcp_servers.portfolio.tools import search_evidence, get_case_study, list_skills
from mcp_servers.marketplace.server import search_jobs_tool, get_job_tool, submit_proposal_tool, create_proposal_draft_tool
from mcp_servers.workspace.server import get_calendar_availability_tool, create_interview_hold_tool
from agent.mcp_client import MCPClientManager, AGENT_TOOL_ALLOWLISTS

def test_portfolio_search_evidence():
    evidence = search_evidence("Python classification scikit-learn", k=3)
    assert len(evidence) > 0
    assert "evidence_id" in evidence[0]
    assert "outcome" in evidence[0]
    assert evidence[0]["type"] in ["case_study", "repository", "past_proposal"]

def test_portfolio_get_case_study():
    case = get_case_study("cs-ai-01")
    assert "content" in case
    assert "Executive Summary" in case["content"]

def test_portfolio_list_skills():
    skills = list_skills("ai_engineer")
    assert "Python" in skills
    assert "scikit-learn" in skills or "PyTorch" in skills

def test_marketplace_read_job():
    jobs = search_jobs_tool(query="churn", limit=5)
    assert len(jobs) > 0
    first_job_id = jobs[0]["job_id"]
    job = get_job_tool(first_job_id)
    assert job["job_id"] == first_job_id
    assert "connects_cost" in job

def test_marketplace_idempotency_and_dry_run():
    jobs = search_jobs_tool(limit=1)
    target_job = jobs[0]
    idempotency_key = f"test-key-{uuid.uuid4().hex}"

    # Dry run
    dry_result = submit_proposal_tool(
        job_id=target_job["job_id"],
        bid_amount_usd=target_job["budget"]["max"],
        estimated_duration_days=14,
        cover_letter="This is an evidence-grounded proposal for testing dry-run verification.",
        evidence_ids=["cs-ai-01"],
        idempotency_key=idempotency_key,
        dry_run=True
    )
    assert dry_result["dry_run"] is True
    assert "connects_cost" in dry_result

    # Real submission
    real_result1 = submit_proposal_tool(
        job_id=target_job["job_id"],
        bid_amount_usd=target_job["budget"]["max"],
        estimated_duration_days=14,
        cover_letter="This is an evidence-grounded proposal for testing dry-run verification.",
        evidence_ids=["cs-ai-01"],
        idempotency_key=idempotency_key,
        dry_run=False
    )
    assert "proposal_id" in real_result1
    assert real_result1["connects_spent"] > 0

    # Retried submission with same idempotency key must return exact same result without spending Connects twice
    real_result2 = submit_proposal_tool(
        job_id=target_job["job_id"],
        bid_amount_usd=target_job["budget"]["max"],
        estimated_duration_days=14,
        cover_letter="This is an evidence-grounded proposal for testing dry-run verification.",
        evidence_ids=["cs-ai-01"],
        idempotency_key=idempotency_key,
        dry_run=False
    )
    assert real_result2["proposal_id"] == real_result1["proposal_id"]
    assert real_result2["remaining_connects"] == real_result1["remaining_connects"]

def test_workspace_availability_and_hold():
    slots = get_calendar_availability_tool(days_ahead=3)
    assert len(slots) > 0
    assert "start_time" in slots[0]

    hold = create_interview_hold_tool(slots[0]["start_time"], "Alex Client", "ML Project")
    assert hold["status"] == "tentative_hold"
    assert hold["client_name"] == "Alex Client"

@pytest.mark.asyncio
async def test_agent_tool_allowlist_enforcement():
    mgr = MCPClientManager()
    # Scout is allowed to search jobs
    assert mgr.is_tool_allowed("scout", "search_jobs") is True
    # Scout is NOT allowed to submit proposal
    assert mgr.is_tool_allowed("scout", "submit_proposal") is False

    with pytest.raises(PermissionError):
        await mgr.execute_tool("scout", "submit_proposal", {"job_id": "test"})

