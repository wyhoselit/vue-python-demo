## 1. Verify Service-Level Telemetry Export

- [x] 1.1 Check `fastapi-backend` logs for OpenTelemetry initialization and export errors.
- [x] 1.2 Check `frontend` logs for OpenTelemetry initialization and export errors. (frontend = nginx, no app logs to check; JS telemetry in bundle)
- [x] 1.3 Verify `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable is correctly set in both services to point to the collector (`http://otel-collector:4318`). (Added to backend in docker-compose.yml)

## 2. Verify OTel Collector Ingestion

- [x] 2.1 Inspect `otel-collector` logs to confirm data is being received from services (look for output from the `logging` exporter).
- [x] 2.2 If no data is received, verify network connectivity between services and collector within the Docker network. (Not needed, data is being received)

## 3. Verify OTel Collector to Backend Exporting

- [x] 3.1 Check `otel-collector` logs for errors exporting traces to Tempo (`tempo:4317`).
- [x] 3.2 Check `otel-collector` logs for errors exporting metrics to Prometheus (verify the `/metrics` endpoint on port 8889 is working).
- [x] 3.3 Check `otel-collector` logs for errors exporting logs to Loki (`http://loki:3100/api/v1/push`).

## 4. Verify Backend Tool Configuration

- [x] 4.1 Access Prometheus UI (`http://localhost:9090`) and check `Status -> Targets`. Ensure `otel-collector` target is `UP`. (User confirmed)
- [x] 4.2 Access Grafana UI (`http://localhost:3000`) and verify datasource configurations for Prometheus, Tempo, and Loki are correct and connection tests pass. (User confirmed)
- [x] 4.3 Use Grafana Explore to query for data in each datasource (e.g., `http_server_requests_seconds_count` in Prometheus, service names in Tempo/Loki). (User confirmed some data, issues remain)

## 5. Document Findings and Fixes

- [x] 5.1 Record the root cause and the fix applied.
- [x] 5.2 Update `docs/telemetry-verification.md` with any new troubleshooting steps or configuration changes required for a healthy setup.