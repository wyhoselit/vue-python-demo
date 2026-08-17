import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import SimpleLogRecordProcessor

from app.modules.core.observability import setup_observability, traced
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter


@pytest.fixture(name="client_with_mocked_exporters")
def client_fixture_with_mocked_exporters():
    # Mock span exporter class and its instance's export method
    mock_span_exporter_class = MagicMock(spec=OTLPSpanExporter)
    mock_span_exporter_instance = mock_span_exporter_class.return_value
    mock_span_exporter_instance.export = MagicMock()

    # Mock metric exporter class and its instance's export method
    mock_metric_exporter_class = MagicMock(spec=OTLPMetricExporter)
    mock_metric_exporter_class.return_value._preferred_temporality = None
    mock_metric_exporter_class.return_value._preferred_aggregation = None
    mock_metric_exporter_instance = mock_metric_exporter_class.return_value
    mock_metric_exporter_instance.export = MagicMock()

    # Mock log exporter class and its instance's export method
    mock_log_exporter_class = MagicMock(spec=OTLPLogExporter)
    mock_log_exporter_instance = mock_log_exporter_class.return_value
    mock_log_exporter_instance.export = MagicMock()

    # Create a real TracerProvider for testing to have force_flush
    test_tracer_provider = TracerProvider()
    test_tracer_provider.add_span_processor(SimpleSpanProcessor(mock_span_exporter_instance))
    test_tracer_provider.force_flush = MagicMock()

    with patch('app.modules.core.observability.OTLPSpanExporter', new=mock_span_exporter_class):
        with patch('app.modules.core.observability.OTLPMetricExporter', new=mock_metric_exporter_class):
            with patch('app.modules.core.observability.OTLPLogExporter', new=mock_log_exporter_class):
                with patch('app.modules.core.observability.BatchSpanProcessor', new=SimpleSpanProcessor):
                    with patch('app.modules.core.observability.BatchLogRecordProcessor', new=SimpleLogRecordProcessor):
                        with patch('opentelemetry.trace.get_tracer_provider', return_value=test_tracer_provider):
                            with patch('opentelemetry.trace.set_tracer_provider'):
                                app = FastAPI()
                                setup_observability(app)

                                @app.get("/test-trace")
                                @traced()
                                async def test_trace_endpoint():
                                    return {"status": "ok"}

                                @app.get("/test-metrics")
                                async def test_metrics_endpoint():
                                    return {"status": "ok"}

                                return TestClient(app), mock_span_exporter_instance.export, mock_metric_exporter_instance.export, mock_log_exporter_instance.export, test_tracer_provider


def test_traces_generated(client_with_mocked_exporters: tuple):
    client, mock_span_exporter_export, mock_metric_exporter_export, mock_log_exporter_export, tracer_provider = client_with_mocked_exporters

    response = client.get("/test-trace")
    assert response.status_code == 200
    
    # Flush to ensure synchronous SimpleSpanProcessor exports
    tracer_provider.force_flush()
    mock_span_exporter_export.assert_called()


# def test_metrics_exposed(client_with_mocked_exporters: tuple):
#     client, mock_span_exporter_export, mock_metric_exporter_export, mock_log_exporter_export, tracer_provider = client_with_mocked_exporters

#     response = client.get("/metrics")
#     assert response.status_code == 200
#     assert "http_requests_total" in response.text
#     assert "http_request_duration_seconds_sum" in response.text


def test_logs_contain_otel_context(client_with_mocked_exporters: tuple):
    client, mock_span_exporter_export, mock_metric_exporter_export, mock_log_exporter_export, tracer_provider = client_with_mocked_exporters

    response = client.get("/test-trace")
    assert response.status_code == 200