"""Worker scheduler coordinating periodic background tasks with graceful shutdown."""

import asyncio
import logging
import signal
from typing import Optional

from worker.tasks import WorkerTaskManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("gigbid.worker.scheduler")

class WorkerScheduler:
    def __init__(self, scout_interval_seconds: int = 60, sync_interval_seconds: int = 120):
        self.scout_interval = scout_interval_seconds
        self.sync_interval = sync_interval_seconds
        self.task_manager = WorkerTaskManager()
        self.is_running = False
        self._stop_event = asyncio.Event()

    async def _scout_loop(self):
        while not self._stop_event.is_set():
            try:
                res = await self.task_manager.run_scout_and_draft_task(persona="ai_engineer")
                logger.info(f"Scout loop cycle completed: {res}")
            except Exception as e:
                logger.error(f"Error in scout cycle: {e}")
            
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.scout_interval)
            except asyncio.TimeoutError:
                pass

    async def _sync_loop(self):
        while not self._stop_event.is_set():
            try:
                res = await self.task_manager.run_sync_pipeline_task()
                logger.info(f"Pipeline sync cycle completed: {res}")
            except Exception as e:
                logger.error(f"Error in sync cycle: {e}")

            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.sync_interval)
            except asyncio.TimeoutError:
                pass

    async def start(self):
        self.is_running = True
        logger.info(f"Starting WorkerScheduler (scout={self.scout_interval}s, sync={self.sync_interval}s)...")
        await asyncio.gather(
            self._scout_loop(),
            self._sync_loop()
        )

    def stop(self):
        logger.info("Stopping WorkerScheduler gracefully...")
        self.is_running = False
        self._stop_event.set()
