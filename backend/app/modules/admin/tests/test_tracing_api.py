import pytest
from starlette.testclient import TestClient
from app.modules.admin.models.trace.trace_configuration import TraceConfiguration
from app.modules.user.user import User
from app.modules.admin.models.role.role import Role
from app.modules.core.security import hash_password

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
        config = TraceConfiguration(service_name="admin", enabled=True)
        db.add(config)
        db.commit()

        response = admin_client.get("/api/v1/admin/tracing/config")
        assert response.status_code == 200
        assert response.json() == {"enabled": True}

    def test_update_tracing_config_success(self, admin_client, db):
        # Test updating to False via query param
        response = admin_client.put("/api/v1/admin/tracing/config?enabled=false")
        assert response.status_code == 200
        assert response.json() == {"enabled": False}

        # Verify in DB
        config = db.query(TraceConfiguration).filter_by(service_name="admin").first()
        assert config.enabled is False

    def test_update_tracing_config_create_if_not_exists(self, admin_client, db):
        # Clear existing configs
        db.query(TraceConfiguration).delete()
        db.commit()

        response = admin_client.put("/api/v1/admin/tracing/config?enabled=true")
        assert response.status_code == 200
        assert response.json() == {"enabled": True}

        config = db.query(TraceConfiguration).filter_by(service_name="admin").first()
        assert config is not None
        assert config.enabled is True

    def test_update_tracing_config_missing_param(self, admin_client):
        # FastAPI returns 422 for missing required query params
        response = admin_client.put("/api/v1/admin/tracing/config")
        assert response.status_code == 422
