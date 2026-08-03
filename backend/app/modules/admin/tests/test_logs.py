import pytest
from starlette.testclient import TestClient
from unittest.mock import patch, mock_open, MagicMock
import json
from app.modules.admin.models.trace.trace_configuration import TraceConfiguration
from app.modules.user.user import User
from app.modules.admin.models.role.role import Role
from app.modules.core.security import hash_password

# (cd /code/vue-python-demo/backend; uv run pytest -v app/modules/admin/tests/test_logs.py::TestLogsAPI)
class TestLogsAPI:
    @pytest.fixture
    def admin_client(self, client: TestClient, db):
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

    def test_get_tracing_logs_redaction(self, admin_client, db):
        mock_log_lines = [
            json.dumps({"level": "INFO", "message": "Login", "password": "secret_password"}),
        ]
        mock_file_content = "\n".join(mock_log_lines)
        
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data=mock_file_content)):
            
            response = admin_client.get("/api/v1/admin/logs")
            assert response.status_code == 200
            log = response.json()["logs"][0]
            assert log["password"] == "[REDACTED]"
