from logging import getLogger
from os import environ

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from pythonjsonlogger import jsonlogger

# 服務名稱，將在 Otel 中顯示
SERVICE_NAME = environ.get("SERVICE_NAME", "backend-service")

# Otel Collector 的 gRPC 端點
OTEL_COLLECTOR_ENDPOINT = environ.get("OTEL_COLLECTOR_ENDPOINT", "otel-collector:4317")


def setup_telemetry(app, engine):
    """
    為 FastAPI 應用程式設定 OpenTelemetry。
    """
    # 1. 資源設定
    resource = Resource.create(
        {
            "service.name": SERVICE_NAME,
            "service.version": "0.1.0",
        }
    )

    # 2. Trace 提供者設定
    tracer_provider = TracerProvider(resource=resource)
    span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=OTEL_COLLECTOR_ENDPOINT, insecure=True))
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)

    # 3. Metric 提供者設定
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=OTEL_COLLECTOR_ENDPOINT, insecure=True)
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    # 注意：在 OpenTelemetry 1.0+ 中，不需要 `metrics.set_meter_provider(meter_provider)`

    # 4. Log 提供者設定
    # 我們將使用 python-json-logger 並通過 LoggingInstrumentor 將 trace context 注入 logs
    log_instrumentor = LoggingInstrumentor()
    log_instrumentor.instrument()

    # 配置 logger 以使用 jsonlogger
    log = getLogger()
    handler = log.handlers[0]
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s %(otelTraceID)s %(otelSpanID)s"
    )
    handler.setFormatter(formatter)

    # 5. 儀器化
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider, meter_provider=meter_provider)
    HTTPXClientInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument(engine=engine)
    SystemMetricsInstrumentor().instrument()

    # 返回 meter_provider 以便在應用程式中手動創建 meters
    return meter_provider

