# opentelemetry-logging Specification

## Purpose
TBD - created by archiving change opentelemetry-injection. Update Purpose after archive.
## Requirements
### Requirement: Loki Deployment
The system SHALL deploy Loki as a container service for log aggregation.

#### Scenario: Loki Starts Successfully
- **WHEN** `compose-up` is executed (using either docker-compose or podman-compose)
- **THEN** the `loki` container SHALL be in a "healthy" state and accessible via port 3100.

### Requirement: Log Ingestion
Loki SHALL be able to ingest logs exported by the OpenTelemetry Collector.

#### Scenario: Ingest OTLP Logs
- **WHEN** the OTel Collector forwards logs to Loki
- **THEN** Loki SHALL successfully store and index these logs.

### Requirement: Log Querying
The system SHALL allow querying of aggregated logs.

#### Scenario: Query Logs by Label
- **WHEN** a user queries logs in Grafana (or directly via Loki API) using a label (e.g., `service="backend"`)
- **THEN** relevant log entries SHALL be returned and displayed.

