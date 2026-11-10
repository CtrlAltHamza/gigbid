from fastapi import APIRouter, HTTPException
from typing import Any
from mcp_servers.marketplace.server import engine

router = APIRouter(prefix="/api/proposals", tags=["proposals"])

@router.get("")
def list_pipeline_proposals():
    """Returns proposals grouped for the Kanban pipeline board."""
    all_props = engine.proposals.values()
    return [p.model_dump() for p in all_props]

@router.get("/{proposal_id}")
def get_proposal_detail(proposal_id: str):
    prop = engine.proposals.get(proposal_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return prop.model_dump()

