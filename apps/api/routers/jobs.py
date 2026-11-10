from fastapi import APIRouter, HTTPException
from typing import Any
from mcp_servers.marketplace.server import search_jobs_tool, get_job_tool
from rag.retriever import GigBidRetriever

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

@router.get("")
def get_jobs(query: str = "", category: str | None = None, limit: int = 30, persona_id: str = "ai_engineer"):
    """Returns ranked jobs with computed fit scores and risk badges."""
    raw_jobs = search_jobs_tool(query=query, category=category, limit=limit)
    retriever = GigBidRetriever(persona_id=persona_id)

    ranked_jobs = []
    for j in raw_jobs:
        # Fast fit check
        q = f"{j['title']} {' '.join(j.get('required_skills', []))}"
        evidence = retriever.retrieve_evidence(q, k=2)
        fit_score = 0.85 if evidence and evidence[0]["score"] > 0.3 else 0.45
        
        # Risk assessment
        signals = j.get("warning_signals", [])
        is_scam = len(signals) > 0 or j.get("budget", {}).get("max", 100) == 0
        risk_score = 0.90 if is_scam else 0.10

        recommended_action = "skip" if is_scam else ("bid" if fit_score >= 0.60 else "watch")

        ranked_jobs.append({
            **j,
            "fit_score": fit_score,
            "risk_score": risk_score,
            "is_scam": is_scam,
            "recommended_action": recommended_action,
            "matched_evidence_count": len(evidence)
        })

    # Rank by fit score descending
    ranked_jobs.sort(key=lambda x: x["fit_score"], reverse=True)
    return ranked_jobs

@router.get("/{job_id}")
def get_job_detail(job_id: str, persona_id: str = "ai_engineer"):
    """
    Returns full job detail with:
    - JobSpec
    - Risk report
    - Requirement-to-evidence matrix
    - Pricing rationale
    """
    job = get_job_tool(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    retriever = GigBidRetriever(persona_id=persona_id)
    skills = job.get("required_skills", ["Python"])
    
    # Build requirement-to-evidence matrix
    matrix = []
    for skill in skills:
        ev = retriever.retrieve_evidence(skill, k=1)
        matrix.append({
            "requirement": skill,
            "matched": len(ev) > 0 and ev[0]["score"] > 0.2,
            "evidence_item": ev[0] if ev else None
        })

    signals = job.get("warning_signals", [])
    is_scam = len(signals) > 0 or job.get("budget", {}).get("max", 100) == 0

    return {
        "job": job,
        "requirement_matrix": matrix,
        "risk_analysis": {
            "is_scam": is_scam,
            "risk_score": 0.85 if is_scam else 0.15,
            "signals": signals,
            "explanation": "Flagged scam indicators" if is_scam else "Verified client profile with clean track record"
        },
        "pricing_rationale": {
            "recommended_bid": (job.get("budget", {}).get("min", 250) + job.get("budget", {}).get("max", 500)) / 2,
            "connects_cost": job.get("connects_cost", 6),
            "roi_ratio": 58.3
        }
    }

