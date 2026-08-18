import pytest
from starlette.testclient import TestClient
from sqlalchemy.exc import OperationalError


def test_health_check_root(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_health_check_v1(client: TestClient):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_health_check_db_failure(monkeypatch):
    from app.main import create_app
    from app.modules.core.observability import setup_observability
    from starlette.testclient import TestClient
    from sqlalchemy.orm import Session
    from unittest.mock import MagicMock
    from app.modules.core.database import get_db

    def get_db_override():
        mock_session = Session(bind=None)
        mock_session.execute = MagicMock(side_effect=OperationalError("SELECT 1", {}, "Database connection failed"))
        yield mock_session

    app = create_app(lifespan=None)
    setup_observability(app)
    app.dependency_overrides[get_db] = get_db_override
    
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 503
        assert "Database connection error" in response.json()["detail"]
    
    app.dependency_overrides.clear()