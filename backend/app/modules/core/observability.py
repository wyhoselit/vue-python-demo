from logging import getLogger
from os import environ
import socket
from urllib.parse import urlparse
from functools import wraps
from typing import Callable, Any
import logging
from pythonjsonlogger import jsonlogger

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from app.modules.core.config import settings
from prometheus_fastapi_instrumentator import Instrumentator

# 服務名稱，將在 Otel 中顯示
tracer = trace.get_tracer(__name__)


def is_otel_collector_available(endpoint: str = settings.OTEL_COLLECTOR_ENDPOINT, timeout: float = 1.0) -> bool:
    logging.getLogger(__name__).info(f"Checking OTEL Collector gRPC endpoint: {endpoint}...")
    try:
        parsed_url = urlparse(endpoint)
        hostname = parsed_url.hostname or endpoint.split(':')[0]
        port = parsed_url.port or int(endpoint.split(':')[1]) if ':' in endpoint else 4317 # Default gRPC port

        if not hostname or not port:
            logging.getLogger(__name__).error(f"OTEL Collector gRPC endpoint {endpoint} is malformed.")
            return False

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((hostname, port))
        sock.close()
        if result == 0:
            logging.getLogger(__name__).info(f"OTEL Collector gRPC endpoint {endpoint} is available.")
            return True
        else:
            logging.getLogger(__name__).warning(f"OTEL Collector gRPC endpoint {endpoint} is NOT available. Connection error: {result}")
            return False
    except Exception as e:
        logging.getLogger(__name__).error(f"Error checking OTEL Collector gRPC availability at {endpoint}: {e}")
        return False

def traced(name: str = None):
    def decorator(func: Callable) -> Callable:
        span_name = name or func.__name__
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            with tracer.start_as_current_span(span_name) as span:
                span.set_attribute("function", func.__name__)
                return await func(*args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            with tracer.start_as_current_span(span_name) as span:
                span.set_attribute("function", func.__name__)
                return func(*args, **kwargs)
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator


def setup_observability(app: FastAPI, engine=None):
    logging.getLogger(__name__).info("Setting up observability...")
    """
    為 FastAPI 應用程式設定 OpenTelemetry。
    """
    resource = Resource.create(
        {
            "service.name": settings.SERVICE_NAME,
            "service.version": "0.1.0",
        }
    )

    otlp_grpc_endpoint = settings.OTEL_COLLECTOR_ENDPOINT
    otlp_http_endpoint = settings.OTEL_COLLECTOR_HTTP_ENDPOINT
    
    if not otlp_http_endpoint.startswith("http://") and not otlp_http_endpoint.startswith("https://"):
        otlp_connectivity_check_endpoint = f"http://{otlp_http_endpoint}"
    else:
        otlp_connectivity_check_endpoint = otlp_http_endpoint

    otel_available = is_otel_collector_available(endpoint=otlp_connectivity_check_endpoint)
    logging.getLogger(__name__).info(f"OTEL Collector available: {otel_available} at {otlp_connectivity_check_endpoint}")

    if otel_available:
        # Trace provider
        tracer_provider = TracerProvider(resource=resource)
        span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_grpc_endpoint, insecure=True))
        tracer_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(tracer_provider)
        
        # Metric provider
        metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(endpoint=otlp_grpc_endpoint, insecure=True)
        )
        meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])

        # Log provider
        logger_provider = LoggerProvider(resource=resource)
        log_exporter = OTLPLogExporter(endpoint=otlp_grpc_endpoint, insecure=True)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
        set_logger_provider(logger_provider)
        
        # Clear existing handlers and add OtelHandler to the root logger
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s %(otelTraceID)s %(otelSpanID)s"
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

        FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider, meter_provider=meter_provider)
    else:
        meter_provider = MeterProvider(resource=resource)
        FastAPIInstrumentor.instrument_app(app, meter_provider=meter_provider)

    # Instrumentations
    HTTPXClientInstrumentor().instrument()
    if engine is not None:
        SQLAlchemyInstrumentor().instrument(engine=engine)
    SystemMetricsInstrumentor().instrument()


    logging.getLogger(__name__).info("Observability setup complete.")
    return meter_provider
