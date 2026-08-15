import socket
from urllib.parse import urlparse
from functools import wraps
from typing import Callable, Any
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from app.modules.core.config import settings
from prometheus_fastapi_instrumentator import Instrumentator

# Setup Prometheus instrumentation at module level (before app creation)


tracer = trace.get_tracer(__name__)

def is_otel_collector_available(endpoint: str = settings.OTEL_COLLECTOR_ENDPOINT, timeout: float = 1.0) -> bool:
    try:
        # Prepend 'http://' if scheme is missing for urlparse to work correctly
        if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
            endpoint = f"http://{endpoint}"

        parsed_url = urlparse(endpoint)
        hostname = parsed_url.hostname
        port = parsed_url.port
        if not hostname or not port:
            return False
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((hostname, port))
        sock.close()
        return result == 0
    except Exception:
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

def setup_observability(app: FastAPI):
    resource = Resource(attributes={"service.name": "fastapi-backend"})
    
    otel_collector_endpoint = settings.OTEL_COLLECTOR_ENDPOINT

    # For gRPC exporters, use the raw endpoint (e.g., "host:port").
    # For HTTP-based connectivity check or HTTP OTLP exporters, prepend "http://".
    otlp_grpc_endpoint = otel_collector_endpoint
    
    if not otel_collector_endpoint.startswith("http://") and not otel_collector_endpoint.startswith("https://"):
        otlp_connectivity_check_endpoint = f"http://{otel_collector_endpoint}"
    else:
        otlp_connectivity_check_endpoint = otel_collector_endpoint

    otel_available = is_otel_collector_available(endpoint=otlp_connectivity_check_endpoint)
    if otel_available:
        trace_provider = TracerProvider(resource=resource)
        otlp_span_exporter = OTLPSpanExporter(
            endpoint=otlp_grpc_endpoint,
            insecure=True,
        )
        
        trace_provider.add_span_processor(BatchSpanProcessor(otlp_span_exporter))
        trace.set_tracer_provider(trace_provider)
        
        otlp_metric_exporter = OTLPMetricExporter(
            endpoint=otlp_grpc_endpoint,
            insecure=True,
        )
        metric_reader = PeriodicExportingMetricReader(otlp_metric_exporter)
        meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
        
        logger_provider = LoggerProvider(resource=resource)
        otlp_log_exporter = OTLPLogExporter(
            endpoint=otlp_grpc_endpoint,
            insecure=True,
        )
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_log_exporter))

        FastAPIInstrumentor().instrument_app(app, tracer_provider=trace_provider, meter_provider=meter_provider)
    else:
        meter_provider = MeterProvider(resource=resource)
        FastAPIInstrumentor().instrument_app(app, meter_provider=meter_provider)
    
    Instrumentator().instrument(app).expose(app)
