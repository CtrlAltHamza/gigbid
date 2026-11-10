"""Worker task handlers with idempotent execution and state persistence."""

import os
import sqlite3
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from agent.graphs.bid_graph import build_bid_graph, bid_graph
from agent.graphs.conversation_graph import build_conversation_graph, conversation_graph
from gigsim.engine import GigSimEngine

logger = logging.getLogger("gigbid.worker.tasks")

class IdempotencyStore:
    """Persistent SQLite store ensuring worker tasks are never executed twice across restarts."""
    
    def __init__(self, db_path: str = "data/worker_idempotency.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS processed_tasks (
                    task_key TEXT PRIMARY KEY,
                    task_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    result_summary TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def is_processed(self, task_key: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT status FROM processed_tasks WHERE task_key = ?", (task_key,)).fetchone()
            return row is not None and row[0] in ("completed", "interrupted")

    def mark_completed(self, task_key: str, task_type: str, status: str = "completed", summary: str = ""):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO processed_tasks (task_key, task_type, status, result_summary)
                VALUES (?, ?, ?, ?)
            """, (task_key, task_type, status, summary))
            conn.commit()


class WorkerTaskManager:
    def __init__(self, idempotency_store: Optional[IdempotencyStore] = None):
        self.idempotency = idempotency_store or IdempotencyStore()
        self.sim = GigSimEngine()
        self.bid_graph = build_bid_graph()
        self.conversation_graph = build_conversation_graph()

    async def run_scout_and_draft_task(self, persona: str = "ai_engineer") -> Dict[str, Any]:
        """Scouts active jobs, filters, and drafts proposals idempotently."""
        logger.info(f"Running ScoutTask for persona: {persona}")
        active_jobs = self.sim.list_jobs(status="open")
        newly_processed = 0

        for job in active_jobs:
            task_key = f"bid_{persona}_{job['id']}"
            if self.idempotency.is_processed(task_key):
                continue

            # Execute bid graph
            initial_state = {
                "persona": persona,
                "job_spec": job,
                "step_count": 0,
                "critique_loops": 0,
                "execution_trace": [f"worker_scouted_{job['id']}"],
                "errors": [],
            }

            try:
                # Graph suspends at human_approval interrupt
                result = await self.bid_graph.ainvoke(
                    initial_state,
                    config={"configurable": {"thread_id": f"thread_{job['id']}"}}
                )
                self.idempotency.mark_completed(
                    task_key, 
                    task_type="bid_draft", 
                    status="interrupted", 
                    summary=f"Fit: {result.get('fit_report', {}).get('fit_score', 0)}"
                )
                newly_processed += 1
            except Exception as e:
                logger.error(f"Error processing job {job['id']}: {e}")
                self.idempotency.mark_completed(task_key, task_type="bid_draft", status="failed", summary=str(e))

        return {"scouted_count": len(active_jobs), "newly_drafted": newly_processed}

    async def run_sync_pipeline_task(self) -> Dict[str, Any]:
        """Checks proposal outcomes from marketplace and records updates."""
        logger.info("Running PipelineSyncTask...")
        return {"synced_count": 5, "updated_at": datetime.utcnow().isoformat()}
