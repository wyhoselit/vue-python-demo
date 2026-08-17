---
type: Documentation
title: Observability Overview
description: Comprehensive documentation for the application's observability stack, including OpenTelemetry, metrics, tracing, logging, and Grafana dashboards for both frontend and backend.
tags: [observability, opentelemetry, metrics, tracing, logging, grafana, prometheus, loki, tempo, frontend, backend]
---

# Observability Overview

This application is instrumented with a robust observability stack using OpenTelemetry to provide insights into its behavior, performance, and health. This includes metrics, distributed tracing, and centralized logging, visualized through Grafana.

## Key Components

The observability stack consists of the following tools, orchestrated via Docker Compose:

-   **OpenTelemetry Collector**: Receives, processes, and exports telemetry data from the application.
    -   Configuration: `dockerdata/observability/otel-collector/collector-config.yml`
-   **Prometheus**: Time-series database for storing and querying metrics.
    -   Configuration: `dockerdata/observability/prometheus/prometheus.yml`
-   **Loki**: Log aggregation system for centralized logging.
    -   Configuration: `dockerdata/observability/loki/loki-config.yml`
-   **Tempo**: High-volume, distributed tracing backend.
    -   Configuration: `dockerdata/observability/tempo/tempo-config.yml`
-   **Grafana**: Data visualization and dashboarding platform.
    -   Configuration: `dockerdata/observability/grafana/provisioning/` (dashboards and datasources)

## Frontend Observability

The frontend application uses OpenTelemetry to capture performance and user interaction metrics.

-   **Instrumentation**: `frontend/src/modules/core/observability.ts`
-   **Metrics Definition**: `frontend/src/modules/core/metrics/metrics.ts`
-   **Component Render Metrics**: `frontend/src/modules/core/metrics/useComponentRenderMetrics.ts`
-   **User Interaction Metrics**: `frontend/src/modules/core/metrics/useMetrics.ts`
-   **Grafana Dashboard**: `dockerdata/observability/grafana/provisioning/dashboards/frontend-observability.json`
-   **E2E Tests**: `frontend/cypress/e2e/observability.cy.ts`

## Backend Observability

The FastAPI backend is instrumented with OpenTelemetry for tracing, metrics, and structured logging.

-   **Instrumentation**: `backend/app/modules/core/observability.py`
-   **Logging**: `backend/app/modules/core/logging.py` (integrates with OpenTelemetry for trace context)
-   **Grafana Dashboards**:
    -   `dockerdata/observability/grafana/provisioning/dashboards/backend-observability.json`
    -   `dockerdata/observability/grafana/provisioning/dashboards/Overall-observability.json`

## Verifying Observability

To verify the observability setup:

1.  Ensure all Docker services are running: `docker compose up`
2.  Access Grafana at `http://localhost:3000` (default credentials `admin`/`admin`).
3.  Explore the provisioned dashboards (Frontend Observability, Backend Observability, Overall Observability) to see metrics, logs, and traces.
4.  Run frontend E2E tests:
    ```bash
    cd frontend
    npm install # if not already installed
    npx cypress run --browser chrome --spec "cypress/e2e/observability.cy.ts"
    ```
    This will generate traffic and metrics visible in Grafana.
5.  Refer to `docs/telemetry-verification.md` for detailed verification steps and expected outputs.
