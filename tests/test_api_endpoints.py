"""Integration tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_list_facilities_endpoint():
    response = client.get("/api/v1/facilities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    first = data[0]
    assert "id" in first
    assert "name" in first
    assert "criticality" in first

def test_list_events_endpoint():
    response = client.get("/api/v1/events")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5

def test_get_event_detail_endpoint():
    response = client.get("/api/v1/events/EVT-2026-IND-042")
    assert response.status_code == 200
    data = response.json()
    assert data["event"]["id"] == "EVT-2026-IND-042"
    assert data["facility"] is not None
    assert data["deviations"] is not None
    assert data["uncertainty"] is not None
    assert data["priority"] is not None
    assert len(data["evidence"]) > 0

def test_get_evaluation_metrics_endpoint():
    response = client.get("/api/v1/evaluation")
    assert response.status_code == 200
    data = response.json()
    assert "ablation_study" in data
    assert "holdout_validation" in data
    assert "adversarial_tests" in data

def test_export_report_endpoint():
    response = client.post(
        "/api/v1/reports/export",
        json={"event_id": "EVT-2026-IND-042", "format": "markdown"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["event_id"] == "EVT-2026-IND-042"
    assert "Forensic Thermal Intelligence Report" in data["content"]
