import pytest
from starlette.testclient import TestClient


def test_http_exception_handler(client: TestClient):
    response = client.get("/non-existent-path")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_general_exception_handler(client: TestClient):
    pass