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


def test_dashboard_realtime_endpoint(client: TestClient):
    response = client.get("/api/v1/dashboard/realtime")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    point = data[0]
    assert "timestamp" in point
    assert "requests" in point
    assert "avgResponseTime" in point
    assert "status2xx" in point
    assert "status4xx" in point
    assert "status5xx" in point
    assert "activeUsers" in point


def test_dashboard_realtime_camelcase_fields(client: TestClient):
    response = client.get("/api/v1/dashboard/realtime")
    assert response.status_code == 200
    data = response.json()
    point = data[0]
    assert isinstance(point["timestamp"], str)
    assert isinstance(point["requests"], int)
    assert isinstance(point["avgResponseTime"], (int, float))
    assert isinstance(point["status2xx"], int)
    assert isinstance(point["status4xx"], int)
    assert isinstance(point["status5xx"], int)
    assert isinstance(point["activeUsers"], int)


def test_dashboard_realtime_value_ranges(client: TestClient):
    response = client.get("/api/v1/dashboard/realtime")
    assert response.status_code == 200
    data = response.json()
    point = data[0]
    assert 0 <= point["requests"] <= 1000
    assert 0 <= point["avgResponseTime"] <= 100
    assert 0 <= point["status2xx"] <= 100
    assert 0 <= point["status4xx"] <= 100
    assert 0 <= point["status5xx"] <= 100
    assert 0 <= point["activeUsers"] <= 100