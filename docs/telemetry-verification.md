# Telemetry Export Verification

This document outlines how to verify that metrics, traces, and logs are being correctly exported to their respective backends after setting up the observability stack.

## Prerequisites
- The full application stack is running via `docker-compose -f docker-compose.yml -f docker-compose.override.yml up`.
- You have generated some traffic to the application (e.g., by running load tests or manually browsing).

## 1. Verify Metrics in Prometheus

### Steps
1. **Open Prometheus UI**: Navigate to `http://localhost:9090`.
2. **Check Targets**: Go to `Status -> Targets`. Both `otel-collector` and `fastapi-backend` jobs should show a state of `UP`.
3. **Query Metrics**: In the expression browser, enter a query for a metric from the FastAPI app, such as `http_server_requests_seconds_count`.
4. **Expected Result**: You should see a graph with data points, indicating that metrics are being scraped successfully.

## 2. Verify Traces in Tempo/Jaeger

### Steps
1. **Open Grafana**: Navigate to `http://localhost:3000`.
2. **Explore with Tempo**:
   - Go to the `Explore` view.
   - Select the `Tempo` or `Jaeger` datasource from the dropdown.
   - Click `Run Query` or use the search to find traces.
3. **Expected Result**: You should see a list of recent traces. Clicking on a trace should display its full span hierarchy, including spans from both the frontend and backend.

## 3. Verify Logs in Loki

### Steps
1. **Open Grafana**: Navigate to `http://localhost:3000`.
2. **Explore with Loki**:
   - Go to the `Explore` view.
   - Select the `Loki` datasource.
   - Use a LogQL query like `{service="backend"}` or `{service="frontend"}` to filter logs.
3. **Expected Result**: You should see log entries from the corresponding service, enriched with OpenTelemetry context like `trace_id` and `span_id`.

## Troubleshooting

- **No Metrics**:
  - Verify the `/metrics` endpoint on the backend (`http://localhost:8000/metrics`) is active.
  - Check Prometheus target status and configuration.
  - Inspect OTel Collector logs for metric processing errors.

- **No Traces**:
  - Ensure the `OTLPTraceExporter` is correctly configured in both frontend and backend.
  - Check OTel Collector logs for trace ingestion and export errors.
  - Verify the Tempo/Jaeger datasource in Grafana is correctly configured to point to `tempo:3200`.

- **No Logs**:
  - Ensure the `OTLPLogExporter` is configured in the backend.
  - Check OTel Collector logs for log processing and export errors.
  - Verify the Loki datasource in Grafana is correctly configured to point to `loki:3100`.
