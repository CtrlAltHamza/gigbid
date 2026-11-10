import json
import os
import re
import time
import uuid
import datetime
from typing import Any
from gigsim.models import Job, Client, ProposalSubmission, ProposalRecord, Message

GENERIC_OPENINGS = [
    r"dear\s+hiring\s+manager",
    r"i\s+am\s+writing\s+to\s+apply",
    r"i\s+am\s+a\s+passionate",
    r"excited\s+to\s+apply",
    r"hope\s+this\s+message\s+finds\s+you\s+well",
    r"to\s+whom\s+it\s+may\s+concern",
    r"hello\s+sir/madam",
]

class GigSimEngine:
    def __init__(self, data_dir: str | None = None):
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.jobs: dict[str, Job] = {}
        self.clients: dict[str, Client] = {}
        self.historical_jobs: list[dict[str, Any]] = []
        self.proposals: dict[str, ProposalRecord] = {}
        self.idempotency_store: dict[str, dict[str, Any]] = {}
        self.messages: dict[str, list[Message]] = {} # thread_id -> messages
        self.connects_balance: dict[str, int] = {"default": 120} # freelancer_id -> balance
        self.rate_limit_tracker: dict[str, list[float]] = {}
        self.max_rpm = 60
        self.error_injection_rate = 0.0 # Can be toggled for chaos testing

        self._load_seed_data()

    def _load_seed_data(self):
        jobs_path = os.path.join(self.data_dir, "jobs.json")
        clients_path = os.path.join(self.data_dir, "clients.json")
        historical_path = os.path.join(self.data_dir, "historical_jobs.json")

        if os.path.exists(jobs_path):
            try:
                with open(jobs_path, "r", encoding="utf-8") as f:
                    raw_jobs = json.load(f)
                    for item in raw_jobs:
                        job = Job(**item)
                        self.jobs[job.job_id] = job
            except Exception as e:
                print(f"[GigSimEngine] Warning loading jobs: {e}")

        if os.path.exists(clients_path):
            try:
                with open(clients_path, "r", encoding="utf-8") as f:
                    raw_clients = json.load(f)
                    for item in raw_clients:
                        client = Client(**item)
                        self.clients[client.client_id] = client
            except Exception as e:
                print(f"[GigSimEngine] Warning loading clients: {e}")

        if os.path.exists(historical_path):
            try:
                with open(historical_path, "r", encoding="utf-8") as f:
                    self.historical_jobs = json.load(f)
            except Exception as e:
                print(f"[GigSimEngine] Warning loading historical jobs: {e}")

    def check_rate_limit(self, client_ip_or_token: str) -> tuple[bool, int]:
        now = time.time()
        window_start = now - 60.0
        timestamps = self.rate_limit_tracker.get(client_ip_or_token, [])
        timestamps = [t for t in timestamps if t > window_start]
        self.rate_limit_tracker[client_ip_or_token] = timestamps
        
        if len(timestamps) >= self.max_rpm:
            retry_after = int(60.0 - (now - timestamps[0])) + 1
            return False, max(1, retry_after)
            
        timestamps.append(now)
        return True, 0

    def search_jobs(self, query: str = "", category: str | None = None, min_budget: float | None = None, max_budget: float | None = None, limit: int = 50, offset: int = 0) -> list[Job]:
        results = list(self.jobs.values())
        if query:
            q = query.lower()
            results = [j for j in results if q in j.title.lower() or q in j.description.lower() or any(q in s.lower() for s in j.required_skills)]
        if category:
            results = [j for j in results if j.category.lower() == category.lower()]
        if min_budget is not None:
            results = [j for j in results if j.budget.max >= min_budget]
        if max_budget is not None:
            results = [j for j in results if j.budget.min <= max_budget]
        return results[offset:offset + limit]

    def get_job(self, job_id: str) -> Job | None:
        return self.jobs.get(job_id)

    def get_client(self, client_id: str) -> Client | None:
        return self.clients.get(client_id)

    def get_connects_balance(self, freelancer_id: str = "default") -> int:
        return self.connects_balance.get(freelancer_id, 120)

    def evaluate_proposal(self, submission: ProposalSubmission, job: Job, client: Client | None) -> dict[str, Any]:
        """
        Simulated Client Decision Model based on:
        - must_have_skills matching
        - generic openings detection
        - budget ceiling
        - evidence grounding
        """
        score = 0.5
        reasons = []
        is_generic = False

        # 1. Check opening
        cover_letter_lower = submission.cover_letter.lower()
        for pattern in GENERIC_OPENINGS:
            if re.search(pattern, cover_letter_lower):
                is_generic = True
                score -= 0.3
                reasons.append("Generic or boilerplate opening detected.")
                break

        # 2. Check evidence references
        if not submission.evidence_ids:
            score -= 0.25
            reasons.append("No portfolio evidence citations provided.")
        else:
            score += min(0.3, len(submission.evidence_ids) * 0.1)
            reasons.append(f"Cited {len(submission.evidence_ids)} portfolio items.")

        # 3. Check client preferences
        if client:
            prefs = client.hidden_preferences
            if prefs.dislikes_generic_openings and is_generic:
                score -= 0.2
            
            # Budget ceiling check
            if submission.bid_amount_usd > prefs.budget_ceiling:
                score -= 0.4
                reasons.append(f"Bid (${submission.bid_amount_usd}) exceeds client budget ceiling (${prefs.budget_ceiling}).")
            elif submission.bid_amount_usd <= job.budget.max:
                score += 0.15
                reasons.append("Bid aligns within posted budget range.")

            # Must have skills check
            matched_skills = [s for s in prefs.must_have_skills if s.lower() in cover_letter_lower]
            if len(prefs.must_have_skills) > 0:
                skill_ratio = len(matched_skills) / len(prefs.must_have_skills)
                score += (skill_ratio - 0.5) * 0.3

        # Clamp score between 0.05 and 0.95
        final_score = max(0.05, min(0.95, score))
        
        # Determine simulated status
        if final_score >= 0.70:
            status = "hired" if final_score >= 0.85 else "interview"
        elif final_score >= 0.45:
            status = "replied"
        elif final_score >= 0.25:
            status = "viewed"
        else:
            status = "rejected"

        return {
            "evaluation_score": round(final_score, 3),
            "status": status,
            "reasons": reasons,
            "will_reply": status in ["replied", "interview", "hired"],
            "will_hire": status == "hired"
        }

    def submit_proposal(self, submission: ProposalSubmission) -> dict[str, Any]:
        # Idempotency check
        if submission.idempotency_key in self.idempotency_store:
            return self.idempotency_store[submission.idempotency_key]

        job = self.get_job(submission.job_id)
        if not job:
            raise ValueError(f"Job {submission.job_id} not found")

        client = self.get_client(job.client_id)
        connects_cost = job.connects_cost
        freelancer_id = submission.freelancer_id or "default"
        current_balance = self.get_connects_balance(freelancer_id)

        if submission.dry_run:
            # Return preview without deducting connects or storing
            eval_result = self.evaluate_proposal(submission, job, client)
            preview = {
                "dry_run": True,
                "job_id": job.job_id,
                "bid_amount_usd": submission.bid_amount_usd,
                "connects_cost": connects_cost,
                "connects_balance_before": current_balance,
                "connects_balance_after": current_balance - connects_cost,
                "can_afford": current_balance >= connects_cost,
                "simulated_outcome_preview": eval_result["status"],
                "evidence_count": len(submission.evidence_ids),
                "idempotency_key": submission.idempotency_key,
            }
            return preview

        if current_balance < connects_cost:
            raise ValueError(f"Insufficient connects balance ({current_balance} < {connects_cost})")

        # Deduct connects
        self.connects_balance[freelancer_id] = current_balance - connects_cost

        # Evaluate proposal
        eval_result = self.evaluate_proposal(submission, job, client)
        proposal_id = f"prop-{uuid.uuid4().hex[:8]}"

        record = ProposalRecord(
            proposal_id=proposal_id,
            job_id=job.job_id,
            freelancer_id=freelancer_id,
            bid_amount_usd=submission.bid_amount_usd,
            estimated_duration_days=submission.estimated_duration_days,
            cover_letter=submission.cover_letter,
            screening_answers=submission.screening_answers,
            evidence_ids=submission.evidence_ids,
            idempotency_key=submission.idempotency_key,
            connects_spent=connects_cost,
            status=eval_result["status"],
            client_feedback="; ".join(eval_result["reasons"]),
            dry_run=False
        )

        self.proposals[proposal_id] = record

        response_data = {
            "proposal_id": proposal_id,
            "status": record.status,
            "connects_spent": connects_cost,
            "remaining_connects": self.connects_balance[freelancer_id],
            "client_feedback": record.client_feedback,
            "submitted_at": record.submitted_at,
            "evaluation_score": eval_result["evaluation_score"]
        }

        # Cache response for idempotency
        self.idempotency_store[submission.idempotency_key] = response_data
        
        # If client will reply, generate an automated client message into messages thread
        if eval_result["will_reply"]:
            thread_id = f"thread-{job.job_id}"
            welcome_msg = Message(
                message_id=f"msg-{uuid.uuid4().hex[:8]}",
                thread_id=thread_id,
                sender_type="client",
                sender_id=job.client_id,
                recipient_id=freelancer_id,
                content=f"Hi Alex, thanks for your proposal on '{job.title}'. Your cited evidence looks solid. Are you available for a brief sync later this week?",
                intent="interview_request" if eval_result["status"] == "interview" else "question"
            )
            if thread_id not in self.messages:
                self.messages[thread_id] = []
            self.messages[thread_id].append(welcome_msg)

        return response_data

    def get_messages(self, thread_id: str | None = None) -> list[Message]:
        if thread_id:
            return self.messages.get(thread_id, [])
        all_msgs = []
        for msgs in self.messages.values():
            all_msgs.extend(msgs)
        return all_msgs

    def send_message(self, thread_id: str, sender_id: str, recipient_id: str, content: str) -> Message:
        msg = Message(
            message_id=f"msg-{uuid.uuid4().hex[:8]}",
            thread_id=thread_id,
            sender_type="freelancer",
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content
        )
        if thread_id not in self.messages:
            self.messages[thread_id] = []
        self.messages[thread_id].append(msg)
        return msg
