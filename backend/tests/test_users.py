import pytest
from starlette.testclient import TestClient
import logging

def test_users_list(client: TestClient, db):
    from app.models.role import Role
    from app.models.user import User
    from app.core.security import hash_password
    
    admin_role = Role(name="admin")
    db.add(admin_role)
    db.commit()
    
    admin_user = User(
        email="admin@example.com",
        hashed_password=hash_password("admin123")
    )
    db.add(admin_user)
    db.commit()
    
    admin_user.roles.append(admin_role)
    db.commit()
    
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "admin123"}
    )
    access_token = login_response.cookies.get("access_token")
    client.cookies.set("access_token", access_token)
    
    client.post("/api/v1/auth/register", json={"email": "alice@example.com", "password": "password123"})
    client.post("/api/v1/auth/register", json={"email": "bob@example.com", "password": "password123"})
    
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for user in data:
        assert "id" in user
        assert "email" in user
        assert isinstance(user["id"], int)
        assert isinstance(user["email"], str)


def test_users_me(client: TestClient):
    # Register and login
    client.post("/api/v1/auth/register", json={"email": "me@example.com", "password": "password123"})
    login_response = client.post("/api/v1/auth/login", json={"email": "me@example.com", "password": "password123"})
    
    # Extract cookie and set on client
    access_token = login_response.cookies.get("access_token")
    assert access_token, "No access_token cookie in login response"
    client.cookies.set("access_token", access_token)
    
    response = client.get("/api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert data["email"] == "me@example.com"


def test_users_me_unauthorized(client: TestClient):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert "error_code" in response.json()


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