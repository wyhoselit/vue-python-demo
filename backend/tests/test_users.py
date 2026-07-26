import pytest
from starlette.testclient import TestClient


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


def test_auth_register_duplicate(client: TestClient):
    response1 = client.post(
        "/api/v1/auth/register",
        json={"email": "test2@example.com", "password": "password123"},
    )
    assert response1.status_code == 200

    response2 = client.post(
        "/api/v1/auth/register",
        json={"email": "test2@example.com", "password": "password456"},
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "detail" in data


def test_auth_login(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "password123"},
    )
    
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 200