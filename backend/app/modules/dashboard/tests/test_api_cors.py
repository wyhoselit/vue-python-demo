import pytest
from starlette.testclient import TestClient


def test_cors_preflight_request(client: TestClient):
    headers = {
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "Content-Type",
    }
    response = client.options("/health", headers=headers)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers


def test_cors_request_from_allowed_origin(client: TestClient):
    headers = {"Origin": "http://localhost:5173"}
    response = client.get("/health", headers=headers)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"