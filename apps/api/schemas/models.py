from typing import Any, Literal
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str
    password: str | None = None
    persona_id: str = "ai_engineer"

class UserProfile(BaseModel):
    username: str
    persona_id: str
    display_name: str
    hourly_rate_usd: float
    min_project_budget_usd: float
    weekly_connects_budget: int
    connected_marketplace: str = "gigsim"
    autonomy_level: Literal["manual", "semi-autonomous", "auto-skip"] = "semi-autonomous"

class ProposalActionRequest(BaseModel):
    thread_id: str
    action: Literal["approve", "reject", "edit"]
    user_edits: str | None = None
    rejection_reason: str | None = None

class MessageActionRequest(BaseModel):
    thread_id: str
    action: Literal["approve", "reject", "edit"]
    edited_reply: str | None = None

class SettingsUpdateRequest(BaseModel):
    weekly_connects_budget: int | None = None
    autonomy_level: Literal["manual", "semi-autonomous", "auto-skip"] | None = None
    minimum_fit_score: float | None = None
    maximum_risk_score: float | None = None
