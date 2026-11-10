import inspect
import json
from mcp_servers.marketplace.schemas import (
    SearchJobsInput, GetJobInput, GetClientHistoryInput,
    CreateProposalDraftInput, SubmitProposalInput, SendMessageInput
)
from mcp_servers.marketplace.server import mcp as marketplace_mcp
from mcp_servers.portfolio.server import mcp as portfolio_mcp
from mcp_servers.workspace.server import mcp as workspace_mcp

def test_marketplace_tool_schema_contract():
    """Validates required MCP write tool parameters and Pydantic constraints."""
    submit_fields = SubmitProposalInput.model_fields
    assert "job_id" in submit_fields
    assert "bid_amount_usd" in submit_fields
    assert "idempotency_key" in submit_fields
    assert "dry_run" in submit_fields
    assert "cover_letter" in submit_fields
    # Validate positive bid constraint
    has_gt_zero = any(getattr(m, "gt", None) == 0 for m in submit_fields["bid_amount_usd"].metadata)
    assert has_gt_zero is True

    create_fields = CreateProposalDraftInput.model_fields
    assert "idempotency_key" in create_fields
    has_min_len = any(getattr(m, "min_length", None) == 20 for m in create_fields["cover_letter"].metadata)
    assert has_min_len is True

def test_mcp_server_tool_registrations():
    """Assert all expected MCP tools are properly registered across servers."""
    marketplace_tools = [tool.name for tool in marketplace_mcp._tool_manager.list_tools()]
    assert "search_jobs" in marketplace_tools
    assert "get_job" in marketplace_tools
    assert "create_proposal_draft" in marketplace_tools
    assert "submit_proposal" in marketplace_tools
    assert "send_message" in marketplace_tools

    portfolio_tools = [tool.name for tool in portfolio_mcp._tool_manager.list_tools()]
    assert "search_evidence" in portfolio_tools
    assert "get_case_study" in portfolio_tools
    assert "list_skills" in portfolio_tools

    workspace_tools = [tool.name for tool in workspace_mcp._tool_manager.list_tools()]
    assert "get_calendar_availability" in workspace_tools
    assert "create_interview_hold" in workspace_tools
    assert "create_email_draft" in workspace_tools
