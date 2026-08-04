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
        response = admin_client.put("/api/v1/system/config/test.key", json={"new": "data"})
        assert response.status_code == 200
        
        setting = db.query(SystemSetting).filter_by(key="test.key").first()
        assert setting.settings == {"new": "data"}

    def test_get_nonexistent_config(self, admin_client: TestClient):
        response = admin_client.get("/api/v1/system/config/nonexistent")
        assert response.status_code == 200
        assert response.json() is None
