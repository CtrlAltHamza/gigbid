import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.routers.auth import router as auth_router
from apps.api.routers.jobs import router as jobs_router
from apps.api.routers.proposals import router as proposals_router
from apps.api.routers.approvals import router as approvals_router
from apps.api.routers.messages import router as messages_router
from apps.api.routers.runs import router as runs_router
from apps.api.routers.analytics import router as analytics_router
from apps.api.routers.settings import router as settings_router

app = FastAPI(
    title="GigBid Copilot API",
    version="1.0.0",
    description="Full-stack FastAPI backend for GigBid Multi-Agent Freelancer Copilot (AI-4016)"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all typed feature routers
app.include_router(auth_router)
app.include_router(jobs_router)
app.include_router(proposals_router)
app.include_router(approvals_router)
app.include_router(messages_router)
app.include_router(runs_router)
app.include_router(analytics_router)
app.include_router(settings_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "gigbid-api",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apps.api.main:app", host="0.0.0.0", port=8000, reload=True)
