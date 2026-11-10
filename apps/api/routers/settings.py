from fastapi import APIRouter, HTTPException
from apps.api.schemas.models import SettingsUpdateRequest
from agent.memory.store import memory_store
from apps.api.auth.store import user_store

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("")
def get_settings(username: str = "reviewer"):
    user = user_store.get_user(username) or {}
    return {
        "weekly_connects_budget": user.get("weekly_connects_budget", 80),
        "autonomy_level": user.get("autonomy_level", "semi-autonomous"),
        "minimum_fit_score": 0.60,
        "maximum_risk_score": 0.70,
        "connected_marketplace": user.get("connected_marketplace", "gigsim"),
        "saved_searches": [
            "machine learning classification scikit-learn",
            "fastapi backend react typescript",
            "dbt snowflake postgresql"
        ]
    }

@router.post("")
def update_settings(req: SettingsUpdateRequest, username: str = "reviewer"):
    user = user_store.get_user(username)
    if user:
        if req.weekly_connects_budget is not None:
            user["weekly_connects_budget"] = req.weekly_connects_budget
        if req.autonomy_level is not None:
            user["autonomy_level"] = req.autonomy_level
        user_store.set_user(username, user)
    return {"status": "settings_updated", "user": user}

@router.get("/memory")
def get_learned_memory():
    """Memory Viewer: Displays learned style rules and category outcomes."""
    return {
        "style_memory_rules": memory_store.get_style_rules(),
        "outcome_memory": memory_store.memory.get("outcome_memory", {})
    }

@router.delete("/memory/style/{index}")
def delete_learned_style_rule(index: int):
    """Allows user to inspect and delete a learned style rule (Viva Requirement 6)."""
    success = memory_store.delete_style_rule(index)
    if not success:
        raise HTTPException(status_code=404, detail="Rule index not found")
    return {"status": "rule_deleted", "remaining_rules": memory_store.get_style_rules()}
