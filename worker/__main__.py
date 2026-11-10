"""CLI entrypoint for running the GigBid background worker."""

import asyncio
import sys
from worker.scheduler import WorkerScheduler

def main():
    scheduler = WorkerScheduler(scout_interval_seconds=30, sync_interval_seconds=60)
    try:
        asyncio.run(scheduler.start())
    except (KeyboardInterrupt, SystemExit):
        scheduler.stop()
        print("\nWorker stopped cleanly.")

if __name__ == "__main__":
    main()

