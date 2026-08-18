# Observability Domain

Full observability stack using OpenTelemetry (OTel), Prometheus, Loki, Tempo, and Grafana for proactive monitoring, rapid debugging, and system reliability.

## Core Concepts

- **Telemetry Aggregation**: Centralized collection of metrics, logs, and traces via OTel Collector.
- **Service Health Monitoring**: Real-time tracking of service availability (`up` metric) and performance.
- **Performance Budgeting**: SLO/SLA tracking via Grafana dashboards (RPS, error rates, latency).
- **Deployment Safety**: Rolling updates managed via Kubernetes `Deployment` resources.

## Key Terms

- **OTLP**: OpenTelemetry Protocol for transmitting telemetry data.
- **RPS**: Requests Per Second, primary throughput metric.
- **Distributed Trace**: End-to-end request path visibility across service boundaries.
- **Log Correlation**: Linking logs to traces using Trace IDs.
- **Alert Rule**: Condition-based notification (e.g., `HighErrorRate` when > 5%).
- **Rolling Deployment**: Zero-downtime update strategy replacing pods incrementally.

## Implementation Details

### Prometheus Alerts
Configured in `dockerdata/observability/prometheus/alerts.yml`.
- `HighErrorRate`: Triggered when 5xx status codes exceed 5% over 5m.
- `ServiceDown`: Triggered when `up == 0` for 1m.

### Grafana Dashboards
Provisioned via `dockerdata/observability/grafana/provisioning/dashboards/`.
- `backend-observability.json`: Backend health, latency, and RPS.
- `frontend-observability.json`: Frontend component performance and interactions.

### Deployment Configuration
Defined in `kubernetes/backend-deployment.yaml`.
- Uses `kind: Deployment` for automated rolling updates.
- Injects `OTEL_EXPORTER_OTLP_ENDPOINT` for automated instrumentation.

## Edge Cases

- **Collector Backpressure**: Metrics may be dropped if OTel Collector or backends (Prometheus/Loki) are overwhelmed.
- **Trace Context Propagation**: Ensuring Trace IDs are passed across async boundaries (e.g., Dramatiq actors).
- **Metric Cardinality**: High-cardinality labels in Prometheus (e.g., raw User IDs) can degrade storage performance.
- **Log Volume**: Large volumes of structured logs can lead to Lokí ingestion delays.
