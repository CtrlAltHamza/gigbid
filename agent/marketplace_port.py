import os
import yaml
from typing import Protocol, Any, runtime_checkable
from mcp_servers.marketplace.adapters.gigsim import GigSimAdapter
from mcp_servers.marketplace.adapters.upwork_live import UpworkLiveAdapter

@runtime_checkable
class MarketplacePort(Protocol):
    async def search_jobs(self, query: str = "", category: str | None = None, min_budget: float | None = None, max_budget: float | None = None, limit: int = 20) -> list[dict[str, Any]]: ...
    async def get_job(self, job_id: str) -> dict[str, Any]: ...
    async def get_client_history(self, client_id: str) -> dict[str, Any]: ...
    async def get_connects_balance(self, freelancer_id: str = "default") -> dict[str, Any]: ...
    async def create_proposal_draft(self, payload: dict[str, Any], idempotency_key: str) -> dict[str, Any]: ...
    async def submit_proposal(self, payload: dict[str, Any], idempotency_key: str, dry_run: bool = False) -> dict[str, Any]: ...
    async def list_messages(self, thread_id: str | None = None) -> list[dict[str, Any]]: ...
    async def send_message(self, thread_id: str, sender_id: str, recipient_id: str, content: str, idempotency_key: str) -> dict[str, Any]: ...

def get_marketplace_adapter(mode: str | None = None) -> MarketplacePort:
    """
    Factory for marketplace adapter switched strictly by configuration.
    Supports 'gigsim' (default simulator) and 'upwork' (live official MCP).
    """
    if not mode:
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.yaml"))
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f)
                    mode = cfg.get("marketplace", {}).get("mode", "gigsim")
            except Exception:
                mode = os.environ.get("MARKETPLACE_MODE", "gigsim")
        else:
            mode = os.environ.get("MARKETPLACE_MODE", "gigsim")

    if mode == "upwork":
        return UpworkLiveAdapter()
    return GigSimAdapter()
