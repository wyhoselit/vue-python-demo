import pytest
from starlette.testclient import TestClient


def test_dashboard_stats(client: TestClient):
    response = client.get("/api/v1/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_users" in data
    assert "active_sessions" in data
    assert "api_calls_24h" in data
    assert isinstance(data["total_users"], int)
    assert isinstance(data["active_sessions"], int)
    assert isinstance(data["api_calls_24h"], int)