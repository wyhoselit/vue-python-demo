## Context

This design provides the technical implementation details for integrating OpenTelemetry into the FastAPI and Vue.js application, as outlined in the `proposal.md`. The goal is to establish a comprehensive observability solution without altering the core application logic. The current architecture lacks monitoring, making this a critical addition for production readiness.

## Goals / Non-Goals

**Goals:**
- Implement full-stack observability (backend, frontend) using OpenTelemetry.
- Collect metrics, traces, and logs.
- Use Podman Compose to orchestrate all services, ensuring modularity.
- Adhere to the existing application's module structure for all new code.
- Provide unit tests for all new instrumentation logic.

**Non-Goals:**
- Replacing existing logging frameworks immediately. OTel will coexist initially.
- Automatic alert configuration in Prometheus or Grafana.
- Performance optimization of the observability stack itself.

## Decisions

### 1. Backend Instrumentation (FastAPI)

- **Library**: `opentelemetry-instrumentation-fastapi` for auto-instrumentation of HTTP requests.
- **Configuration**: A new module `backend/app/observability.py` will encapsulate all OTel setup. This keeps observability concerns separate from the main application logic, following the existing modular architecture.
- **Exporters**:
  - **Traces/Logs**: Use `OTLPSpanExporter` and `OTLPLogExporter` to send data to the OTel Collector.
  - **Metrics**: Use `PrometheusInstrumentator` to expose a `/metrics` endpoint for Prometheus to scrape.
- **Unit Tests**: Tests will be added in `backend/tests/test_observability.py` to verify that the OTel setup is correct and that instrumented routes produce the expected telemetry.

### 2. Frontend Instrumentation (Vue.js)

- **Library**: `@opentelemetry/sdk-trace-web` and other relevant JS packages.
- **Configuration**: A new module `frontend/src/observability.ts` will handle OTel initialization.
- **Instrumentation**:
  - `@opentelemetry/sdk-metrics` and `@opentelemetry/exporter-metrics-otlp-http` for app-level metrics.
  - `instrumentation-xml-http-request` and `instrumentation-fetch` for tracing browser API calls.
  - Custom wrappers for Vue Router and Pinia will be created to generate spans for navigation and state changes.
- **Exporters**: Use `OTLPTraceExporter` and `OTLPMetricExporter` to send telemetry to the OTel Collector.
- **Unit Tests**: Tests in `frontend/tests/observability.spec.ts` will ensure that user interactions and component lifecycles generate the correct traces and metrics.
- **E2E Tests**: Tests in `frontend/cypress/e2e/observability.cy.ts` will verify that metrics are correctly sent to the OTel Collector.

### 3. Observability Stack Deployment

- **Tool**: Podman Compose will manage all services (auto-detect: prefer podman-compose if available, fallback to docker-compose).
- **Services**:
  - `otel-collector`: Receives data from the app and exports to backends.
  - `prometheus`: Scrapes metrics from the collector and FastAPI app.
  - `grafana`: Visualizes data from Prometheus, Loki, and Jaeger/Tempo.
  - `loki`: Log aggregation.
  - `tempo`: Trace storage and retrieval.
- **Configuration**: Service configurations (`collector.yaml`, `prometheus.yml`) will be managed in a separate `observability/` directory at the project root. This maintains modularity.

## Risks / Trade-offs

- **Performance Overhead**: Introducing instrumentation can add latency.
  - **Mitigation**: Start with default sampling rates and adjust based on performance testing. The OTel SDKs are designed to be lightweight.
- **Configuration Complexity**: The observability stack has many components.
  - **Mitigation**: Provide clear documentation and use a modular `docker-compose.override.yml` to keep the core `docker-compose.yml` clean.
- **Data Volume**: High-traffic applications can generate large amounts of telemetry data.
  - **Mitigation**: Implement sampling and filtering in the OTel Collector to manage data volume and cost.

## Open Questions

- What are the specific business-critical transactions that require custom, detailed spans?
- What is the expected retention period for metrics, logs, and traces?
