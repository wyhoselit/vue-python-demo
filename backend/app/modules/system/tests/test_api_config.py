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
    def test_get_system_config(self, admin_client: TestClient, db):
        new_setting = SystemSetting(
            key="test.key",
            settings={"value": "test_value"}
        )
        db.add(new_setting)
        db.commit()

        response = admin_client.get("/api/v1/system/config/test.key")
        assert response.status_code == 200
        assert response.json() == {"value": "test_value"}

    def test_update_system_config(self, admin_client: TestClient, db):
        new_setting = SystemSetting(
            key="test.key",
            settings={"value": "old_value"}
        )
        db.add(new_setting)
        db.commit()

        response = admin_client.put("/api/v1/system/config/test.key", json={"value": {"new": "data"}})
        assert response.status_code == 200
        
        db.expire_all()
        setting = db.query(SystemSetting).filter_by(key="test.key").first()
        assert setting.settings == {"new": "data"}

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

    def test_get_all_configs_unauthorized(self, client: TestClient):
        response = client.get("/api/v1/system/config/")
        assert response.status_code == 401

    def test_put_nonexistent_config(self, admin_client: TestClient):
        response = admin_client.put("/api/v1/system/config/nonexistent", json={"value": "new"})
        assert response.status_code == 404

    def test_put_invalid_payload(self, admin_client: TestClient):
        response = admin_client.put("/api/v1/system/config/test.key", json={})
        assert response.status_code == 422

    def test_get_all_configs_empty(self, admin_client: TestClient, db):
        response = admin_client.get("/api/v1/system/config/")
        assert response.status_code == 200
        assert response.json() == {}

    def test_get_all_configs_large(self, admin_client: TestClient, db):
        settings = [SystemSetting(key=f"test.key{i}", settings={"value": f"v{i}"}) for i in range(100)]
        db.add_all(settings)
        db.commit()

        response = admin_client.get("/api/v1/system/config/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 100
        assert data["test.key0"] == {"value": "v0"}
        assert data["test.key99"] == {"value": "v99"}
