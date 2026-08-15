## Why

The application currently lacks observability. No metrics, traces, or logs are collected systematically. This makes debugging production issues difficult and prevents performance monitoring. Adding OpenTelemetry integration with FastAPI (backend) and Vue.js (frontend) will provide full-stack observability via Prometheus, Grafana, Jaeger/Tempo, and Loki.

## What Changes

- Add OpenTelemetry Python SDK to FastAPI backend for automatic instrumentation (HTTP requests, database, background tasks)
- Add OpenTelemetry JavaScript SDK to Vue.js frontend for browser metrics, traces, and user interaction tracking
- Deploy OpenTelemetry Collector as middleware to receive, process, and export telemetry data
- Configure Prometheus exporter for metrics collection
- Configure OTLP exporters for traces (Jaeger/Tempo) and logs (Loki)
- Use Podman Compose override to add observability stack without modifying base services (auto-detect: prefer podman-compose if available, fallback to docker-compose).
- Add custom instrumentation for business-critical routes and Pinia/Vuex state changes

## Capabilities

### New Capabilities
- `opentelemetry-backend`: Backend instrumentation with FastAPI auto-instrumentation, custom spans, and metrics
- `opentelemetry-frontend`: Frontend instrumentation with Vue.js lifecycle tracking, router spans, and Pinia state changes
- `opentelemetry-collector`: Collector deployment and configuration for receiving, processing, and exporting telemetry
- `opentelemetry-prometheus`: Prometheus metrics endpoint and scraping configuration
- `opentelemetry-tracing`: Distributed tracing with Jaeger/Tempo backend
- `opentelemetry-logging`: Structured logging with Loki backend

### Modified Capabilities
- `backend-api`: Add OTel middleware and instrumentation hooks
- `frontend-app`: Add OTel initialization and Vue router/Pinia plugins
- `docker-orchestration`: Extend podman-compose/docker-compose with observability services

## Impact

- Backend: FastAPI app, middleware, database layer, background tasks
- Frontend: Vue app entry, router, Pinia stores, API client
- Infrastructure: Podman Compose/Docker Compose, new collector/prometheus/grafana/jaeger/loki services
- Dependencies: opentelemetry-api, opentelemetry-sdk, opentelemetry-instrumentation-fastapi, @opentelemetry/sdk-trace-web, @opentelemetry/exporter-collector