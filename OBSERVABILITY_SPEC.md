## Problem Statement

The project lacks a comprehensive observability solution, making it difficult to monitor system health, diagnose performance bottlenecks, and ensure reliability against defined Service Level Objectives (SLOs). Without metrics, alerting, and visualization, the team cannot proactively identify or react to issues affecting the backend, frontend, or the Nginx proxy.

## Solution

Implement a full observability stack using OpenTelemetry, Prometheus, and Grafana. This will provide deep visibility into all components of the application stack. The solution involves instrumenting the backend and frontend applications to emit OpenTelemetry metrics, scraping Nginx for performance data, and consolidating all metrics for monitoring, alerting, and visualization.

## User Stories

1.  As a DevOps Engineer, I want to monitor backend API latency (P95) and error rates, so that I can ensure the service meets its Latency (< 200ms P95) and Availability (> 99.9%) SLIs.
2.  As a DevOps Engineer, I want to be alerted when backend latency spikes or error rates exceed a defined threshold, so that I can investigate and resolve performance degradations quickly.
3.  As a Frontend Developer, I want to track frontend page load times and user interaction latencies, so that I can optimize the end-user experience.
4.  As a Site Reliability Engineer, I want a unified Grafana dashboard displaying key health metrics for the backend, frontend, and Nginx proxy, so that I can get a holistic view of system status at a glance.
5.  As a Site Reliability Engineer, I want to monitor Nginx active connections, request rates, and response status codes, so that I can identify traffic anomalies or proxy-level issues.
6.  As an On-call Engineer, I want to receive reliable alerts via Alertmanager when any component (backend, frontend, Nginx) is down or performing poorly, so that I can respond to incidents promptly.
7.  As a Developer, I want a reference document (`docs/metrics-reference.md`) that lists all available metrics, so that I can understand what data is available for debugging and analysis.
8.  As a Project Manager, I want to see SLI/SLO compliance reports, so that I can assess the overall reliability of the service.
9.  As a DevOps Engineer, I want all observability components to be managed via `podman-compose`, so that the local development environment is consistent and easy to manage.

## Implementation Decisions

-   **Instrumentation**:
    -   Backend (FastAPI): Use `prometheus-fastapi-instrumentator` to automatically instrument the application and export metrics in OpenTelemetry format.
    -   Frontend (Vue): Use `@opentelemetry/instrumentation-document-load` and `@opentelemetry/instrumentation-user-interaction` for Real User Monitoring (RUM) metrics.
    -   Nginx: Enable the `stub_status` module and use the `nginx-prometheus-exporter` to scrape its metrics.
-   **Metric Collection**:
    -   An OpenTelemetry Collector (`otel-collector`) will serve as the central metrics gateway.
    -   It will receive OTLP metrics from the backend and frontend.
    -   It will scrape the `nginx-prometheus-exporter` using its Prometheus receiver.
-   **Storage, Alerting, and Visualization**:
    -   Prometheus will scrape the OTel Collector to ingest all system metrics.
    -   Alerting rules for all components will be defined in a central `alerts.yml` file and managed by Prometheus.
    -   Alertmanager will handle alert routing (initial setup focuses on firing, not complex notification pipelines).
    -   Grafana will use Prometheus as its data source for pre-built dashboards covering backend, frontend, and Nginx observability.
-   **Metric Naming**:
    -   The `exported_job` label will be used in the OTel Collector to preserve the original service name (e.g., `backend`, `frontend`), as Prometheus will scrape all metrics from the single `otel-collector` job.
-   **Project Setup**:
    -   The repository is configured to use GitHub Issues, a default triage label vocabulary, and a single-context domain documentation layout as per Matt Pocock's engineering skill standards.

## Testing Decisions

-   **Seams**:
    1.  **Metric Generation**: Verify that each service (backend, frontend, nginx-exporter) correctly generates and exposes metrics.
    2.  **Prometheus Ingestion**: Confirm that Prometheus successfully scrapes the OTel collector and that all metrics are queryable.
    3.  **Alert Firing**: Test Prometheus alert rules by simulating metric conditions (e.g., high latency, errors) and verifying that alerts transition to a `FIRING` state. `promtool check rules` will be used for static validation.
-   **Prior Art**: Testing will follow standard practices for observability pipelines. No specific prior art exists in this codebase, so industry best practices will be the guide. We will focus on end-to-end validation (from instrumentation to dashboard panel) rather than isolated unit tests for individual components.

## Out of Scope

-   **Distributed Tracing**: This spec does not cover the implementation of distributed tracing (e.g., Jaeger, Zipkin).
-   **Log Aggregation**: Centralized logging (e.g., Loki, ELK) is not part of this work.
-   **Production Alertmanager Routing**: Configuring complex notification channels in Alertmanager (e.g., PagerDuty, Slack) is deferred. The goal is to ensure alerts fire correctly.

## Further Notes

-   A known blocker is an Alertmanager container startup failure due to a `permission denied` error on its data volume. This must be resolved by fixing volume permissions (`chown`) or adjusting the Podman security context.
-   The work done for this spec will be used to update the `resume.md` file to reflect the new skills and accomplishments in observability.
