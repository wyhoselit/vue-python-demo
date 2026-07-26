import pytest
from starlette.testclient import TestClient
import logging

def test_users_list(client: TestClient):
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for user in data:
        assert "id" in user
        assert "name" in user
        assert "email" in user
        assert "status" in user
        assert isinstance(user["id"], int)
        assert isinstance(user["name"], str)
        assert isinstance(user["email"], str)
        assert isinstance(user["status"], str)


def test_auth_register(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data


def test_auth_register_duplicate(client: TestClient, caplog):
    client.post(
        "/api/v1/auth/register",
        json={"email": "test2@example.com", "password": "password123"},
    )

    with caplog.at_level(logging.WARNING):
        response2 = client.post(
            "/api/v1/auth/register",
            json={"email": "test2@example.com", "password": "password456"},
        )
    assert response2.status_code == 409
    assert response2.json()["error_code"] == "EMAIL_ALREADY_EXISTS"
    assert "Registration failed - email exists" in caplog.text

def test_auth_login_invalid(client: TestClient, caplog):
    client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "password123"},
    )
    
    with caplog.at_level(logging.WARNING):
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "login@example.com", "password": "wrongpassword"},
        )
    assert response.status_code == 401
    assert response.json()["error_code"] == "INVALID_CREDENTIALS"
    assert "Login failed - invalid credentials" in caplog.text

