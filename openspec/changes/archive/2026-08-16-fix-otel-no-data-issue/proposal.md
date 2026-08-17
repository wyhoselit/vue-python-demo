## Why

The current observability setup is not functioning correctly. Users are reporting "No Data" in Grafana and Prometheus, which prevents monitoring of the application's health, performance, and behavior. This change is required to diagnose and fix the telemetry pipeline.

## What Changes

- Verify and correct the configuration of the OpenTelemetry collector.
- Ensure metrics, traces, and logs are being exported from the frontend and backend services.
- Validate that Prometheus, Tempo, and Loki are correctly receiving data from the collector.
- Update documentation if any configuration changes are needed to make the setup work.

## Capabilities

### New Capabilities
- `telemetry-pipeline-verification`: A repeatable process and scripts to verify the health of the observability pipeline.

### Modified Capabilities
- None

## Impact

- **Code**: May require changes to `docker-compose.override.yml`, `otel-collector-config.yaml`, and potentially the frontend/backend service configurations.
- **APIs**: No external API changes.
- **Dependencies**: No new dependencies.
- **Systems**: Affects the local development observability stack (Grafana, Prometheus, Tempo, Loki, OTel Collector).
