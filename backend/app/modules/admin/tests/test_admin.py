import pytest
from starlette.testclient import TestClient
from app.core.database import get_db
from app.modules.admin.models.role.role import Role
from app.modules.user.user import User
from app.core.security import hash_password

def test_admin_system_info_unauthorized(client: TestClient):
    response = client.get("/api/v1/admin/system-info")
    assert response.status_code == 401

def test_admin_system_info_forbidden(client: TestClient):
    client.post("/api/v1/auth/register", json={"email": "user@example.com", "password": "password123"})
    login_response = client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "password123"})
    access_token = login_response.cookies.get("access_token")
    client.cookies.set("access_token", access_token)
    
    response = client.get("/api/v1/admin/system-info")
    assert response.status_code == 403

def test_admin_system_info_success(client: TestClient, db):
    admin_role = Role(name="admin")
    db.add(admin_role)
    db.commit()
    db.refresh(admin_role)
    
    admin_user = User(
        email="admin@example.com",
        hashed_password=hash_password("password123")
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    admin_user.roles.append(admin_role)
    db.commit()
    
    login_response = client.post("/api/v1/auth/login", json={"email": "admin@example.com", "password": "password123"})
    access_token = login_response.cookies.get("access_token")
    client.cookies.set("access_token", access_token)
    
    response = client.get("/api/v1/admin/system-info")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "os" in data
    assert "database" in data