import pytest
from starlette.testclient import TestClient
from app.modules.system.models.system_setting import SystemSetting
from app.modules.user.user import User
from app.modules.admin.models.role.role import Role
from app.modules.core.security import hash_password

@pytest.fixture
def admin_client(client: TestClient, db):
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

class TestSystemConfigAPI:
    def test_get_all_configs(self, admin_client: TestClient, db):
        setting1 = SystemSetting(key="test.key1", settings={"value": "v1"})
        setting2 = SystemSetting(key="test.key2", settings={"value": "v2"})
        db.add_all([setting1, setting2])
        db.commit()

        response = admin_client.get("/api/v1/system/config/")
        assert response.status_code == 200
        data = response.json()
        assert data["test.key1"] == {"value": "v1"}
        assert data["test.key2"] == {"value": "v2"}

    def test_get_all_configs_empty(self, admin_client: TestClient, db):
        response = admin_client.get("/api/v1/system/config/")
        assert response.status_code == 200
        assert response.json() == {}

    def test_get_all_configs_with_existing(self, admin_client: TestClient, db):
        existing = SystemSetting(key="system.tracing", settings={"enabled": True})
        db.add(existing)
        db.commit()

        response = admin_client.get("/api/v1/system/config/")
        assert response.status_code == 200
        data = response.json()
        assert "system.tracing" in data
        assert data["system.tracing"]["enabled"] == True
