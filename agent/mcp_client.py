import os
import asyncio
import logging
from typing import Any, Callable
from agent.marketplace_port import get_marketplace_adapter
from mcp_servers.portfolio.tools import search_evidence, get_case_study, list_skills
from mcp_servers.workspace.server import get_calendar_availability_tool, create_interview_hold_tool, create_email_draft_tool

logger = logging.getLogger("gigbid.mcp_client")

# Strict agent allowlists: Each agent gets only the tools it is authorized to call
AGENT_TOOL_ALLOWLISTS: dict[str, list[str]] = {
    "scout": ["search_jobs", "get_job"],
    "analyst": [], # No MCP tools needed; pure JobSpec extraction
    "risk_assessor": ["get_client_history", "get_job"],
    "fit_matcher": ["search_evidence", "get_case_study", "list_skills"],
    "pricing": ["get_client_history", "get_connects_balance"],
    "writer": ["search_evidence", "get_case_study"],
    "verifier": ["search_evidence", "get_case_study"],
    "critic": ["search_evidence", "get_case_study"],
    "compliance": [], # Pure policy validation
    "client_liaison": [
        "list_messages", "send_message",
        "get_calendar_availability", "create_interview_hold", "create_email_draft"
    ]
}

class DegradedModeError(Exception):
    """Raised when an external MCP server is unreachable and system enters degraded mode."""
    pass

class MCPClientManager:
    """
    Manages MCP tool execution across Portfolio, Marketplace, and Workspace servers.
    Enforces per-agent tool filtering, bounded retries with backoff, and degraded mode.
    """
    def __init__(self):
        self.marketplace = get_marketplace_adapter()
        self.degraded_mode = False

    def is_tool_allowed(self, agent_role: str, tool_name: str) -> bool:
        allowed = AGENT_TOOL_ALLOWLISTS.get(agent_role, [])
        return tool_name in allowed

    async def execute_tool(
        self,
        agent_role: str,
        tool_name: str,
        arguments: dict[str, Any],
        max_retries: int = 2
    ) -> Any:
        if not self.is_tool_allowed(agent_role, tool_name):
            raise PermissionError(f"Agent '{agent_role}' is not authorized to invoke tool '{tool_name}'")

        # Bounded retry with exponential backoff
        for attempt in range(max_retries + 1):
            try:
                return await self._dispatch_tool(tool_name, arguments)
            except Exception as e:
                logger.warning(f"Tool '{tool_name}' execution attempt {attempt + 1} failed: {e}")
                if attempt == max_retries:
                    self.degraded_mode = True
                    raise DegradedModeError(f"Tool '{tool_name}' failed after {max_retries} retries: {str(e)}")
                await asyncio.sleep(0.5 * (2 ** attempt))

    async def _dispatch_tool(self, tool_name: str, args: dict[str, Any]) -> Any:
        # Portfolio tools
        if tool_name == "search_evidence":
            return search_evidence(requirement=args.get("requirement", ""), k=args.get("k", 5), persona_id=args.get("persona_id", "ai_engineer"))
        elif tool_name == "get_case_study":
            return get_case_study(case_id=args.get("case_id", ""), persona_id=args.get("persona_id", "ai_engineer"))
        elif tool_name == "list_skills":
            return list_skills(persona_id=args.get("persona_id", "ai_engineer"))

        # Marketplace tools
        elif tool_name == "search_jobs":
            return await self.marketplace.search_jobs(
                query=args.get("query", ""),
                category=args.get("category"),
                min_budget=args.get("min_budget"),
                max_budget=args.get("max_budget"),
                limit=args.get("limit", 20)
            )
        elif tool_name == "get_job":
            return await self.marketplace.get_job(job_id=args["job_id"])
        elif tool_name == "get_client_history":
            return await self.marketplace.get_client_history(client_id=args["client_id"])
        elif tool_name == "get_connects_balance":
            return await self.marketplace.get_connects_balance(freelancer_id=args.get("freelancer_id", "default"))
        elif tool_name == "create_proposal_draft":
            return await self.marketplace.create_proposal_draft(payload=args, idempotency_key=args["idempotency_key"])
        elif tool_name == "submit_proposal":
            return await self.marketplace.submit_proposal(payload=args, idempotency_key=args["idempotency_key"], dry_run=args.get("dry_run", False))
        elif tool_name == "list_messages":
            return await self.marketplace.list_messages(thread_id=args.get("thread_id"))
        elif tool_name == "send_message":
            return await self.marketplace.send_message(
                thread_id=args["thread_id"],
                sender_id=args.get("sender_id", "default"),
                recipient_id=args["recipient_id"],
                content=args["content"],
                idempotency_key=args["idempotency_key"]
            )

        # Workspace tools
        elif tool_name == "get_calendar_availability":
            return get_calendar_availability_tool(
                days_ahead=args.get("days_ahead", 5),
                slot_duration_minutes=args.get("slot_duration_minutes", 30)
            )
        elif tool_name == "create_interview_hold":
            return create_interview_hold_tool(
                slot_time=args["slot_time"],
                client_name=args.get("client_name", "Client"),
                job_title=args.get("job_title", "Interview")
            )
        elif tool_name == "create_email_draft":
            return create_email_draft_tool(
                recipient=args["recipient"],
                subject=args["subject"],
                body=args["body"]
            )
        else:
            raise NotImplementedError(f"Unknown tool '{tool_name}'")

