import os
import json
import datetime
from typing import Any

AUDIT_LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs", "audit_log.jsonl"))

def log_audit_event(
    user: str,
    tool: str,
    arguments: dict[str, Any],
    result: dict[str, Any],
    trace_id: str = "default-trace-id",
    status: str = "success"
):
    """Append-only audit log entry."""
    os.makedirs(os.path.dirname(AUDIT_LOG_FILE), exist_ok=True)
    entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "trace_id": trace_id,
        "user": user,
        "tool": tool,
        "arguments": arguments,
        "result": result,
        "status": status
    }
    with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

