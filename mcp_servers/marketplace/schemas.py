from typing import Any, Literal
from pydantic import BaseModel, Field

class SearchJobsInput(BaseModel):
    query: str = Field(default="", description="Search keywords for job title or description")
    category: str | None = Field(default=None, description="Job category: machine-learning, full-stack, data-analytics")
    min_budget: float | None = Field(default=None, ge=0, description="Minimum budget filter")
    max_budget: float | None = Field(default=None, ge=0, description="Maximum budget filter")
    limit: int = Field(default=20, ge=1, le=100, description="Max jobs to return")

class GetJobInput(BaseModel):
    job_id: str = Field(min_length=1, description="Unique job identifier")

class GetClientHistoryInput(BaseModel):
    client_id: str = Field(min_length=1, description="Unique client identifier")

class GetConnectsBalanceInput(BaseModel):
    freelancer_id: str = Field(default="default", description="Freelancer account ID")

class CreateProposalDraftInput(BaseModel):
    job_id: str = Field(min_length=1, description="Target job identifier")
    freelancer_id: str = Field(default="default", description="Freelancer identifier")
    bid_amount_usd: float = Field(gt=0, description="Proposed fixed bid or hourly amount in USD")
    estimated_duration_days: int = Field(gt=0, le=365, description="Estimated days to deliver")
    cover_letter: str = Field(min_length=20, description="Drafted cover letter grounded in portfolio evidence")
    screening_answers: list[str] = Field(default_factory=list, description="Answers to client screening questions")
    evidence_ids: list[str] = Field(default_factory=list, description="List of cited portfolio evidence IDs")
    idempotency_key: str = Field(min_length=8, description="Unique UUID to prevent duplicate draft creation")

class SubmitProposalInput(BaseModel):
    job_id: str = Field(min_length=1, description="Target job identifier")
    freelancer_id: str = Field(default="default", description="Freelancer identifier")
    bid_amount_usd: float = Field(gt=0, description="Final approved bid in USD")
    estimated_duration_days: int = Field(gt=0, le=365, description="Approved duration in days")
    cover_letter: str = Field(min_length=20, description="Approved proposal text")
    screening_answers: list[str] = Field(default_factory=list, description="Approved screening answers")
    evidence_ids: list[str] = Field(default_factory=list, description="Verified evidence IDs cited")
    idempotency_key: str = Field(min_length=8, description="Unique UUID to guarantee idempotency")
    dry_run: bool = Field(default=False, description="If True, returns exact execution preview without deducting Connects")

class SendMessageInput(BaseModel):
    thread_id: str = Field(min_length=1, description="Conversation thread identifier")
    sender_id: str = Field(min_length=1, description="Sender user ID")
    recipient_id: str = Field(min_length=1, description="Recipient user ID")
    content: str = Field(min_length=1, description="Message text")
    idempotency_key: str = Field(min_length=8, description="Unique UUID to prevent duplicate messages")
    dry_run: bool = Field(default=False, description="If True, preview message without sending")

# Output Schemas
class ProposalResponse(BaseModel):
    proposal_id: str | None = None
    status: str
    connects_spent: int
    remaining_connects: int
    client_feedback: str | None = None
    dry_run: bool = False
    idempotency_key: str

class MessageResponse(BaseModel):
    message_id: str | None = None
    thread_id: str
    sender_id: str
    recipient_id: str
    content: str
    timestamp: str
    status: str = "sent"
    dry_run: bool = False
