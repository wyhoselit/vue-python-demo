import pytest
from starlette.testclient import TestClient
from app.modules.system.models.system_setting import SystemSetting
from app.modules.user.user import User
from app.modules.admin.models.role.role import Role
from app.modules.core.security import hash_password
import json

# (cd /code/vue-python-demo/backend; uv run pytest -v backend/app/modules/admin/tests/test_tracing_api.py::TestTracingAPI)

# (cd /code/vue-python-demo/backend; uv run pytest -v backend/app/modules/admin/tests/test_tracing_api.py::TestTracingAPI)
class TestTracingAPI:
    @pytest.fixture
    def admin_client(self, client: TestClient, db):
        # Create admin role and user
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
        
        # Login as admin
        login_response = client.post("/api/v1/auth/login", json={"email": "admin@example.com", "password": "password123"})
        access_token = login_response.cookies.get("access_token")
        client.cookies.set("access_token", access_token)
        return client

    def test_get_tracing_config(self, admin_client, db):
        # Setup: Ensure a config exists
        from datetime import datetime
        new_setting = SystemSetting(
            key="tracing.admin",
            settings={"enabled": True},
            updated_at=datetime.utcnow()
        )
        db.add(new_setting)
        db.commit()

        response = admin_client.get("/api/v1/admin/tracing/config")
        assert response.status_code == 200
        assert response.json() == {"enabled": True}

    def test_update_tracing_config_success(self, admin_client, db):
        # Test updating to False
        response = admin_client.put("/api/v1/admin/tracing/config?enabled=false")
        assert response.status_code == 200
        assert response.json() == {"enabled": False}

        # Verify in DB
        setting = db.query(SystemSetting).filter_by(key="tracing.admin").first()
        assert setting.settings["enabled"] is False

    def test_update_tracing_config_create_if_not_exists(self, admin_client, db):
        # Clear existing configs
        db.query(SystemSetting).filter_by(key="tracing.admin").delete()
        db.commit()

        response = admin_client.put("/api/v1/admin/tracing/config?enabled=true")
        assert response.status_code == 200
        assert response.json() == {"enabled": True}

        setting = db.query(SystemSetting).filter_by(key="tracing.admin").first()
        assert setting is not None
        assert setting.settings["enabled"] is True

    def test_get_tracing_config_default_disabled(self, admin_client, db):
        # Ensure no config exists
        db.query(SystemSetting).filter_by(key="tracing.admin").delete()
        db.commit()

        response = admin_client.get("/api/v1/admin/tracing/config")
        assert response.status_code == 200
        assert response.json() == {"enabled": False}
