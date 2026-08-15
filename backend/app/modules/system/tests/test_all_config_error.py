import pytest
from starlette.testclient import TestClient
from app.modules.user.user import User
from app.modules.admin.models.role.role import Role
from app.modules.core.security import hash_password

def create_admin_client(client: TestClient, db):
    admin_role = Role(name="admin")
    db.add(admin_role)
    db.commit()
    admin_user = User(
        email="admin@example.com",
        hashed_password=hash_password("password123")
    )
    db.add(admin_user)
    db.commit()
    admin_user.roles.append(admin_role)
    db.commit()
    
    login_response = client.post("/api/v1/auth/login", json={"email": "admin@example.com", "password": "password123"})
    access_token = login_response.cookies.get("access_token")
    client.cookies.set("access_token", access_token)
    return client

class TestSystemConfigAPIErrorHandling:
    def test_get_all_configs_unauthorized(self, client: TestClient):
        # Without auth cookie
        response = client.get("/api/v1/system/config/")
        assert response.status_code == 401

    def test_put_nonexistent_config(self, client: TestClient, db):
        admin_client = create_admin_client(client, db)
        response = admin_client.put("/api/v1/system/config/nonexistent", json={"value": "new"})
        # Assuming the endpoint should return 404 if the key is not found
        assert response.status_code == 404

    def test_put_invalid_payload(self, client: TestClient, db):
        admin_client = create_admin_client(client, db)
        response = admin_client.put("/api/v1/system/config/test.key", json={})
        assert response.status_code == 422
