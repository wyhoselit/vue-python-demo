import pytest
from starlette.testclient import TestClient
from app.core.database import get_db
from app.models.user import User
from app.models.role import Role
from app.core.security import hash_password

def test_admin_system_info_unauthorized(client: TestClient):
    # Test without admin role
    response = client.get("/api/v1/admin/system-info")
    assert response.status_code == 401

def test_admin_system_info_forbidden(client: TestClient):
    # Register a regular user (without admin role) and try to access admin endpoint
    client.post("/api/v1/auth/register", json={"email": "user@example.com", "password": "password123"})
    login_response = client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "password123"})
    
    access_token = login_response.cookies.get("access_token")
    client.cookies.set("access_token", access_token)
    
    response = client.get("/api/v1/admin/system-info")
    assert response.status_code == 403

def test_admin_system_info_success(client: TestClient, db):
    # Create admin role
    admin_role = Role(name="admin")
    db.add(admin_role)
    db.commit()
    db.refresh(admin_role)
    
    # Create admin user
    admin_user = User(
        email="admin@example.com",
        hashed_password=hash_password("password123")
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    # Assign admin role to user
    admin_user.roles.append(admin_role)
    db.commit()
    
    # Login as admin
    login_response = client.post("/api/v1/auth/login", json={"email": "admin@example.com", "password": "password123"})
    access_token = login_response.cookies.get("access_token")
    client.cookies.set("access_token", access_token)
    
    response = client.get("/api/v1/admin/system-info")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "os" in data
    assert "database" in data