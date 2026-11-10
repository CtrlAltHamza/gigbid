from typing import Any, Literal
from pydantic import BaseModel, Field
import datetime

class Budget(BaseModel):
    min: float = 0.0
    max: float = 0.0
    currency: str = "USD"
    type: Literal["fixed", "hourly"] = "fixed"

class Job(BaseModel):
    job_id: str
    client_id: str
    title: str
    description: str
    category: str
    required_skills: list[str] = Field(default_factory=list)
    budget: Budget
    duration_days: int = 14
    screening_questions: list[str] = Field(default_factory=list)
    warning_signals: list[str] = Field(default_factory=list)
    connects_cost: int = 6
    posted_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    status: Literal["open", "in_review", "closed"] = "open"
    planted_injection: bool = False

class ClientPreferences(BaseModel):
    must_have_skills: list[str] = Field(default_factory=list)
    budget_ceiling: float = 1000.0
    dislikes_generic_openings: bool = True
    dislikes_missing_evidence: bool = True
    min_freelancer_rating: float = 4.0
    reply_probability_base: float = 0.4
    hire_probability_base: float = 0.25

class Client(BaseModel):
    client_id: str
    name: str
    company_type: str = "Startup"
    country: str = "United States"
    completed_projects: int = 5
    total_spent_usd: float = 12500.0
    average_rating: float = 4.85
    payment_verified: bool = True
    member_since: str = "2023-01-15"
    hidden_preferences: ClientPreferences = Field(default_factory=ClientPreferences)

class ProposalSubmission(BaseModel):
    job_id: str
    freelancer_id: str
    bid_amount_usd: float = Field(gt=0)
    estimated_duration_days: int = Field(gt=0)
    cover_letter: str = Field(min_length=20)
    screening_answers: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    dry_run: bool = False
    idempotency_key: str

class ProposalRecord(BaseModel):
    proposal_id: str
    job_id: str
    freelancer_id: str
    bid_amount_usd: float
    estimated_duration_days: int
    cover_letter: str
    screening_answers: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    idempotency_key: str
    connects_spent: int
    status: Literal["draft", "submitted", "viewed", "replied", "interview", "hired", "rejected"] = "submitted"
    submitted_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    client_feedback: str | None = None
    dry_run: bool = False

class Message(BaseModel):
    message_id: str
    thread_id: str
    sender_type: Literal["client", "freelancer", "system"]
    sender_id: str
    recipient_id: str
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    intent: str | None = None

