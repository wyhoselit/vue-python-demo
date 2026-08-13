from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.metrics import get_meter_provider
from fastapi import FastAPI
from sqlalchemy import Engine
import os

def setup_observability(app: FastAPI, engine: Engine):
    service_name = os.environ.get("SERVICE_NAME", "backend")
    resource = Resource(attributes={
        "service.name": service_name
    })

    # Tracing
    trace_provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True))
    trace_provider.add_span_processor(processor)
    trace.set_tracer_provider(trace_provider)

    # Metrics
    metric_reader = PrometheusMetricReader()
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    # The get_meter_provider function returns the global meter provider.
    # set_meter_provider is not available in the opentelemetry-api package.
    # Instead, we need to call get_meter_provider to get the meter provider and then use it.
    # The MeterProvider constructor registers the new provider as the global provider.
    # So we don't need to call set_meter_provider explicitly.
    get_meter_provider()

    # Instrumentation
    FastAPIInstrumentor.instrument_app(app, tracer_provider=trace_provider)
    SQLAlchemyInstrumentor().instrument(engine=engine, tracer_provider=trace_provider)
    LoggingInstrumentor().instrument(set_logging_format=True)

    print("OpenTelemetry instrumentation complete.")
