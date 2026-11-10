import uuid
import datetime
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("gigbid-workspace-server")

# In-memory holds and drafts store (can integrate with Google Workspace API or run local mock)
interview_holds: list[dict[str, Any]] = []
email_drafts: list[dict[str, Any]] = []

@mcp.tool(
    name="get_calendar_availability",
    description="Find available interview slots in the freelancer's calendar for client meetings."
)
def get_calendar_availability_tool(
    days_ahead: int = 5,
    slot_duration_minutes: int = 30
) -> list[dict[str, Any]]:
    """Generate upcoming free interview slots."""
    slots = []
    base_date = datetime.date.today()
    for day_offset in range(1, days_ahead + 1):
        target_date = base_date + datetime.timedelta(days=day_offset)
        # Skip weekends (Saturday=5, Sunday=6)
        if target_date.weekday() >= 5:
            continue
        for hour in [14, 16, 18]: # 2 PM, 4 PM, 6 PM UTC
            slot_iso = datetime.datetime(target_date.year, target_date.month, target_date.day, hour, 0, tzinfo=datetime.timezone.utc).isoformat()
            slots.append({
                "slot_id": f"slot-{target_date.strftime('%Y%m%d')}-{hour}",
                "start_time": slot_iso,
                "duration_minutes": slot_duration_minutes,
                "status": "available"
            })
    return slots[:6]

@mcp.tool(
    name="create_interview_hold",
    description="Place a tentative interview hold on the calendar for a client conversation."
)
def create_interview_hold_tool(
    slot_time: str,
    client_name: str,
    job_title: str
) -> dict[str, Any]:
    """Create a tentative calendar hold."""
    hold_id = f"hold-{uuid.uuid4().hex[:8]}"
    hold = {
        "hold_id": hold_id,
        "slot_time": slot_time,
        "client_name": client_name,
        "job_title": job_title,
        "status": "tentative_hold",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    interview_holds.append(hold)
    return hold

@mcp.tool(
    name="create_email_draft",
    description="Create an email draft in Gmail / workspace client for client correspondence."
)
def create_email_draft_tool(
    recipient: str,
    subject: str,
    body: str
) -> dict[str, Any]:
    """Draft an email."""
    draft_id = f"email-draft-{uuid.uuid4().hex[:8]}"
    draft = {
        "draft_id": draft_id,
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "status": "draft_created",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    email_drafts.append(draft)
    return draft

if __name__ == "__main__":
    mcp.run()
