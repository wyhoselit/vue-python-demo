import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@patch('app.observability.OTLPSpanExporter')
@patch('app.observability.PrometheusMetricReader')
def test_health_check_generates_telemetry(MockPrometheusMetricReader, MockOTLPSpanExporter, client):
    """
    Tests that a simple endpoint like /health generates telemetry data.
    """
    # Mock the exporters to avoid actual network calls
    mock_span_exporter_instance = MockOTLPSpanExporter.return_value
    mock_span_exporter_instance.export = MagicMock()

    # When the health check endpoint is called
    response = client.get("/health")

    # Then the response should be successful
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    # And spans should have been exported
    # In a real scenario, we might inspect the calls, but here we just check if export was called.
    # Due to batching, this might not be called on every request, so this is a simplification.
    # A more robust test would involve a more complex setup with a test-only in-memory exporter.
    assert mock_span_exporter_instance.export.called
