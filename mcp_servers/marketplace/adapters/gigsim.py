import os
import httpx
from typing import Any
from gigsim.engine import GigSimEngine
from gigsim.models import ProposalSubmission

class GigSimAdapter:
    """Marketplace adapter communicating with GigSim Simulator."""
    def __init__(self, base_url: str | None = None, api_token: str | None = None):
        self.base_url = base_url or os.environ.get("GIGSIM_BASE_URL", "http://localhost:8081")
        self.api_token = api_token or os.environ.get("GIGSIM_API_TOKEN", "mock-token")
        self.engine = GigSimEngine() # Fallback to in-process engine if HTTP server not running

    async def search_jobs(self, query: str = "", category: str | None = None, min_budget: float | None = None, max_budget: float | None = None, limit: int = 20) -> list[dict[str, Any]]:
        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=5.0) as client:
                resp = await client.get("/jobs", params={"query": query, "category": category, "min_budget": min_budget, "max_budget": max_budget, "limit": limit})
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        # In-process fallback
        jobs = self.engine.search_jobs(query=query, category=category, min_budget=min_budget, max_budget=max_budget, limit=limit)
        return [j.model_dump() for j in jobs]

    async def get_job(self, job_id: str) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=5.0) as client:
                resp = await client.get(f"/jobs/{job_id}")
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        job = self.engine.get_job(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
        return job.model_dump()

    async def get_client_history(self, client_id: str) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=5.0) as client:
                resp = await client.get(f"/clients/{client_id}")
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        client = self.engine.get_client(client_id)
        if not client:
            raise ValueError(f"Client {client_id} not found")
        data = client.model_dump()
        data.pop("hidden_preferences", None)
        return data

    async def get_connects_balance(self, freelancer_id: str = "default") -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=5.0) as client:
                resp = await client.get("/connects/balance", params={"freelancer_id": freelancer_id})
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        return {"freelancer_id": freelancer_id, "balance": self.engine.get_connects_balance(freelancer_id)}

    async def create_proposal_draft(self, payload: dict[str, Any], idempotency_key: str) -> dict[str, Any]:
        # Local draft generation
        job = await self.get_job(payload["job_id"])
        return {
            "draft_id": f"draft-{idempotency_key[:8]}",
            "job_id": payload["job_id"],
            "freelancer_id": payload.get("freelancer_id", "default"),
            "bid_amount_usd": payload.get("bid_amount_usd", job.get("budget", {}).get("max", 500)),
            "cover_letter": payload.get("cover_letter", ""),
            "status": "draft",
            "connects_required": job.get("connects_cost", 6),
            "idempotency_key": idempotency_key
        }

    async def submit_proposal(self, payload: dict[str, Any], idempotency_key: str, dry_run: bool = False) -> dict[str, Any]:
        try:
            body = {**payload, "idempotency_key": idempotency_key, "dry_run": dry_run}
            async with httpx.AsyncClient(base_url=self.base_url, timeout=5.0) as client:
                resp = await client.post("/proposals", json=body)
                if resp.status_code in [200, 201]:
                    return resp.json()
        except Exception:
            pass
        sub = ProposalSubmission(
            job_id=payload["job_id"],
            freelancer_id=payload.get("freelancer_id", "default"),
            bid_amount_usd=payload["bid_amount_usd"],
            estimated_duration_days=payload.get("estimated_duration_days", 14),
            cover_letter=payload["cover_letter"],
            screening_answers=payload.get("screening_answers", []),
            evidence_ids=payload.get("evidence_ids", []),
            dry_run=dry_run,
            idempotency_key=idempotency_key
        )
        return self.engine.submit_proposal(sub)

    async def list_messages(self, thread_id: str | None = None) -> list[dict[str, Any]]:
        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=5.0) as client:
                resp = await client.get("/messages", params={"thread_id": thread_id} if thread_id else {})
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        msgs = self.engine.get_messages(thread_id)
        return [m.model_dump() for m in msgs]

    async def send_message(self, thread_id: str, sender_id: str, recipient_id: str, content: str, idempotency_key: str) -> dict[str, Any]:
        try:
            body = {"thread_id": thread_id, "sender_id": sender_id, "recipient_id": recipient_id, "content": content}
            async with httpx.AsyncClient(base_url=self.base_url, timeout=5.0) as client:
                resp = await client.post("/messages", json=body)
                if resp.status_code in [200, 201]:
                    return resp.json()
        except Exception:
            pass
        msg = self.engine.send_message(thread_id, sender_id, recipient_id, content)
        return msg.model_dump()

