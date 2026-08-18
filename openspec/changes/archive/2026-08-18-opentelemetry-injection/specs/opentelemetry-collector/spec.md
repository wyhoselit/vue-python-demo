## ADDED Requirements

### Requirement: OTel Collector Deployment
The system SHALL deploy the OpenTelemetry Collector as a container service.

#### Scenario: Collector Starts Successfully
- **WHEN** `compose-up` is executed (using either docker-compose or podman-compose)
- **THEN** the `otel-collector` container SHALL be in a "healthy" state and listening on port 4317 (gRPC) and 4318 (HTTP).

### Requirement: Compose Command Detection
The deployment scripts SHALL use `docker-compose` on systems where it is available, falling back to `podman-compose` if necessary.

#### Scenario: Auto-Detect Compose Tool
- **WHEN** the deployment script is run
- **THEN** it SHALL first check for `podman-compose`, then fall back to `docker-compose` if available.

### Requirement: OTLP Receiver Configuration
The system SHALL configure the Collector to receive OTLP data from backend and frontend.

#### Scenario: Receive Backend Traces
- **WHEN** the backend sends OTLP traces to the Collector on port 4317
- **THEN** the Collector SHALL accept the traces and forward them to the tracing exporter.

#### Scenario: Receive Frontend Traces
- **WHEN** the frontend sends OTLP traces to the Collector on port 4318
- **THEN** the Collector SHALL accept the traces and forward them to the tracing exporter.

### Requirement: Collector Exporters Configuration
The system SHALL configure exporters for Prometheus (metrics), Tempo/Jaeger (traces), and Loki (logs).

#### Scenario: Export Metrics to Prometheus
- **WHEN** the Collector receives metrics
- **THEN** the metrics SHALL be available for scraping by Prometheus.

#### Scenario: Export Traces to Tempo
- **WHEN** the Collector receives traces
- **THEN** the traces SHALL be forwarded to Tempo.

#### Scenario: Export Logs to Loki
- **WHEN** the Collector receives logs
- **THEN** the logs SHALL be forwarded to Loki.
