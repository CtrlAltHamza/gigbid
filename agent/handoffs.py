from typing import Any, Literal
from pydantic import BaseModel, Field

class JobSpec(BaseModel):
    job_id: str
    title: str
    deliverables: list[str] = Field(default_factory=list)
    required_skills: list[str] = Field(default_factory=list)
    budget_min: float | None = None
    budget_max: float | None = None
    duration_days: int = 14
    screening_questions: list[str] = Field(default_factory=list)
    hidden_needs: list[str] = Field(default_factory=list)
    connects_cost: int = 6

class RiskReport(BaseModel):
    score: float = Field(ge=0, le=1, description="0.0 (safe) to 1.0 (extreme risk)")
    flags: list[str] = Field(default_factory=list)
    explanation: str
    is_scam: bool = False
    has_injection: bool = False

class FitReport(BaseModel):
    score: float = Field(ge=0, le=1, description="0.0 to 1.0 match ratio")
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    rationale: str = ""

class BidDecision(BaseModel):
    action: Literal["bid", "watch", "skip"]
    confidence: float = Field(ge=0, le=1)
    reasons: list[str] = Field(default_factory=list)

class PriceQuote(BaseModel):
    recommended_bid_usd: float = Field(gt=0)
    connects_cost: int
    expected_roi: float = Field(ge=0)
    rationale: str

class ProposalDraft(BaseModel):
    job_id: str
    freelancer_id: str = "default"
    cover_letter: str
    screening_answers: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    revision_count: int = 0
    status: str = "draft"

class Critique(BaseModel):
    passed: bool
    score: float = Field(ge=0, le=1)
    revision_reasons: list[str] = Field(default_factory=list)
    suggested_edits: str | None = None

class ComplianceVerdict(BaseModel):
    compliant: bool
    violations: list[str] = Field(default_factory=list)
    sanitized_draft: str
