from fastapi import APIRouter, HTTPException
from apps.api.schemas.models import LoginRequest, UserProfile
from apps.api.auth.store import user_store

router = APIRouter(prefix="/api/auth", tags=["auth"])

PERSONA_PROFILES = [
    {
        "persona_id": "ai_engineer",
        "display_name": "Alex Rivera",
        "title": "Lead AI/ML Engineer",
        "hourly_rate_usd": 65.0,
        "min_project_budget_usd": 400.0,
        "category": "machine-learning"
    },
    {
        "persona_id": "fullstack_dev",
        "display_name": "Sarah Chen",
        "title": "Senior Full-Stack Web Developer",
        "hourly_rate_usd": 60.0,
        "min_project_budget_usd": 350.0,
        "category": "full-stack"
    },
    {
        "persona_id": "data_analyst",
        "display_name": "Marcus Vance",
        "title": "Principal Data Analyst & BI Specialist",
        "hourly_rate_usd": 55.0,
        "min_project_budget_usd": 300.0,
        "category": "data-analytics"
    }
]

@router.get("/personas")
def list_personas():
    return PERSONA_PROFILES

@router.post("/login", response_model=UserProfile)
def login(req: LoginRequest):
    user = user_store.get_user(req.username)
    if not user:
        # Auto-create user session initialized with selected persona
        selected_p = next((p for p in PERSONA_PROFILES if p["persona_id"] == req.persona_id), PERSONA_PROFILES[0])
        user = {
            "username": req.username,
            "persona_id": req.persona_id,
            "display_name": selected_p["display_name"],
            "hourly_rate_usd": selected_p["hourly_rate_usd"],
            "min_project_budget_usd": selected_p["min_project_budget_usd"],
            "weekly_connects_budget": 80,
            "connected_marketplace": "gigsim",
            "autonomy_level": "semi-autonomous"
        }
        user_store.set_user(req.username, user)

    return UserProfile(**user)

@router.get("/me", response_model=UserProfile)
def get_current_user(username: str = "reviewer"):
    user = user_store.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfile(**user)
