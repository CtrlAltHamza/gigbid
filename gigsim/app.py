import os
import random
from fastapi import FastAPI, HTTPException, Request, Response, Header
from fastapi.middleware.cors import CORSMiddleware
from gigsim.engine import GigSimEngine
from gigsim.models import Job, Client, ProposalSubmission, ProposalRecord, Message

app = FastAPI(title="GigSim Marketplace Simulator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = GigSimEngine()

@app.middleware("http")
async def check_rate_limits_and_errors(request: Request, call_next):
    # Skip rate limiting on health check or admin
    if request.url.path in ["/health", "/docs", "/openapi.json"]:
        return await call_next(request)

    client_id = request.headers.get("Authorization", request.client.host if request.client else "unknown")
    allowed, retry_after = engine.check_rate_limit(client_id)
    if not allowed:
        return Response(
            content='{"detail": "GigSim rate limit exceeded (max 60 rpm)"}',
            status_code=429,
            media_type="application/json",
            headers={"Retry-After": str(retry_after)}
        )

    # Simulated transient failure if error injection is active
    if engine.error_injection_rate > 0 and random.random() < engine.error_injection_rate:
        return Response(
            content='{"detail": "GigSim transient marketplace error (simulated 503)"}',
            status_code=503,
            media_type="application/json"
        )

    return await call_next(request)

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "gigsim",
        "jobs_count": len(engine.jobs),
        "clients_count": len(engine.clients),
        "proposals_count": len(engine.proposals)
    }

@app.get("/jobs", response_model=list[Job])
def list_jobs(
    query: str = "",
    category: str | None = None,
    min_budget: float | None = None,
    max_budget: float | None = None,
    limit: int = 50,
    offset: int = 0
):
    return engine.search_jobs(query, category, min_budget, max_budget, limit, offset)

@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: str):
    job = engine.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")
    return job

@app.get("/clients/{client_id}", response_model=Client)
def get_client(client_id: str):
    client = engine.get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail=f"Client '{client_id}' not found")
    return client

@app.get("/connects/balance")
def get_connects_balance(freelancer_id: str = "default"):
    return {
        "freelancer_id": freelancer_id,
        "balance": engine.get_connects_balance(freelancer_id)
    }

@app.post("/proposals")
def submit_proposal(submission: ProposalSubmission):
    try:
        return engine.submit_proposal(submission)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/proposals/{proposal_id}", response_model=ProposalRecord)
def get_proposal(proposal_id: str):
    prop = engine.proposals.get(proposal_id)
    if not prop:
        raise HTTPException(status_code=404, detail=f"Proposal '{proposal_id}' not found")
    return prop

@app.get("/proposals", response_model=list[ProposalRecord])
def list_proposals():
    return list(engine.proposals.values())

@app.get("/messages", response_model=list[Message])
def get_messages(thread_id: str | None = None):
    return engine.get_messages(thread_id)

@app.post("/messages", response_model=Message)
def send_message(payload: dict):
    thread_id = payload.get("thread_id", "default")
    sender_id = payload.get("sender_id", "freelancer")
    recipient_id = payload.get("recipient_id", "client")
    content = payload.get("content", "")
    if not content:
        raise HTTPException(status_code=400, detail="Message content cannot be empty")
    return engine.send_message(thread_id, sender_id, recipient_id, content)

@app.get("/stats/historical")
def get_historical_jobs(limit: int = 500, category: str | None = None):
    jobs = engine.historical_jobs
    if category:
        jobs = [j for j in jobs if j.get("category", "").lower() == category.lower()]
    return {"total_count": len(jobs), "sample": jobs[:limit]}

@app.post("/admin/reset")
def reset_state():
    engine.__init__(engine.data_dir)
    return {"status": "reset_successful"}

@app.post("/admin/set_error_rate")
def set_error_rate(rate: float):
    engine.error_injection_rate = max(0.0, min(1.0, rate))
    return {"status": "updated", "error_injection_rate": engine.error_injection_rate}
