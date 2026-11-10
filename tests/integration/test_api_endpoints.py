import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_api_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_api_auth_and_personas():
    res = client.get("/api/auth/personas")
    assert res.status_code == 200
    personas = res.json()
    assert len(personas) == 3
    assert any(p["persona_id"] == "ai_engineer" for p in personas)

    login_res = client.post("/api/auth/login", json={"username": "reviewer", "persona_id": "ai_engineer"})
    assert login_res.status_code == 200
    assert login_res.json()["username"] == "reviewer"

def test_api_jobs_inbox_and_detail():
    res = client.get("/api/jobs")
    assert res.status_code == 200
    jobs = res.json()
    assert len(jobs) > 0
    assert "fit_score" in jobs[0]
    assert "recommended_action" in jobs[0]

    job_id = jobs[0]["job_id"]
    detail_res = client.get(f"/api/jobs/{job_id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert "requirement_matrix" in detail
    assert "pricing_rationale" in detail

def test_api_approvals_and_proposals():
    pending_res = client.get("/api/approvals/pending")
    assert pending_res.status_code == 200
    assert isinstance(pending_res.json(), list)

    props_res = client.get("/api/proposals")
    assert props_res.status_code == 200
    assert isinstance(props_res.json(), list)

def test_api_analytics_and_settings_memory():
    analytics_res = client.get("/api/analytics")
    assert analytics_res.status_code == 200
    data = analytics_res.json()
    assert "reply_and_hire_rates_by_category" in data
    assert "connects_roi" in data

    memory_res = client.get("/api/settings/memory")
    assert memory_res.status_code == 200
    mem_data = memory_res.json()
    assert "style_memory_rules" in mem_data
    assert len(mem_data["style_memory_rules"]) > 0

