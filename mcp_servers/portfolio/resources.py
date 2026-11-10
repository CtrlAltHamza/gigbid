import os
import json
from mcp_servers.portfolio.tools import get_persona_dir, get_case_study

def get_case_resource(case_id: str) -> str:
    """Resource handler for portfolio://case/{id}"""
    try:
        data = get_case_study(case_id)
        return data["content"]
    except Exception as e:
        return f"Error loading case resource '{case_id}': {str(e)}"

def get_proposal_resource(proposal_id: str) -> str:
    """Resource handler for portfolio://proposal/{id}"""
    # Search all personas for proposal
    for p_id in ["ai_engineer", "fullstack_dev", "data_analyst"]:
        p_dir = get_persona_dir(p_id)
        prop_path = os.path.join(p_dir, "proposals.json")
        if os.path.exists(prop_path):
            try:
                with open(prop_path, "r", encoding="utf-8") as f:
                    proposals = json.load(f)
                for p in proposals:
                    if p.get("proposal_id") == proposal_id:
                        return json.dumps(p, indent=2)
            except Exception:
                continue
    return f"Proposal '{proposal_id}' not found."

