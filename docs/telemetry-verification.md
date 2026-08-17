# Telemetry Export Verification

This document outlines how to verify that metrics, traces, and logs are being correctly exported to their respective backends after setting up the observability stack.

## Prerequisites

- The full application stack is running via `docker-compose -f docker-compose.yml -f docker-compose.override.yml up`.
- You have generated some traffic to the application (e.g., by running load tests or manually browsing).
- Ensure the backend has `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable set to point to the OTel Collector (`http://otel-collector:4318`). If not set, add it to `docker-compose.yml`.

## 1. Verify Metrics in Prometheus

### Backend Metrics

### Steps

1. **Open Prometheus UI**: Navigate to `http://localhost:9090`.
2. **Check Targets**: Go to `Status -> Targets`. Both `otel-collector` and `fastapi-backend` jobs should show a state of `UP`.
3. **Query Metrics**: In the expression browser, enter a query for a metric from the FastAPI app. Note: `http_server_requests_seconds_count` is **not** a valid metric name in this setup. Use:
     - `http_requests_total` - Total number of requests
     - `http_request_duration_seconds` - Request duration histogram
     - `http_request_duration_highr_seconds` - Request duration histogram with more buckets
     - `up{job="fastapi-backend"}` - Check if target is being scraped
4. **Expected Result**: You should see a graph with data points, indicating that metrics are being scraped successfully.

### Frontend Metrics

### Steps

1. **Open Prometheus UI**: Navigate to `http://localhost:9090`.
2. **Check Targets**: Go to `Status -> Targets`. The `frontend` job should show a state of `UP`.
3. **Query Metrics**: In the expression browser, enter queries for frontend metrics:
     - `http_client_duration_seconds_count{job="frontend"}` - Total number of HTTP client requests from the frontend
     - `http_client_duration_seconds_bucket{job="frontend"}` - Request duration histogram for frontend API calls
     - `document_load_duration_seconds_bucket` - Page load duration metrics from the frontend
     - `theme_toggle_count` - Custom counter for theme toggle interactions
4. **Expected Result**: You should see a graph with data points, indicating that frontend metrics are being scraped successfully.

### Troubleshooting

- **Metric not found**: 
  - Backend: Check the `/metrics` endpoint directly at `http://localhost:8000/metrics` to see the actual metric names exposed by the application.
  - Frontend: Ensure the frontend is sending metrics to the OTel Collector. Run `curl http://localhost:8889/metrics` to see all metrics received by the collector.
- **No metrics at all**: Ensure the `otel-collector` and `backend` targets are `UP` in Prometheus Targets page. Verify the `PrometheusPipeline` is enabled in OTel Collector.
- **Frontend metrics not appearing**: 
  - Verify `VITE_OTEL_METRICS_ENABLED=true` is set in `docker-compose.yml`.
  - Check that `VITE_OTEL_COLLECTOR_METRICS_URL` points to `http://otel-collector:4318/v1/metrics`.
  - Confirm OTel Collector logs show metrics being received from the frontend.

### Verifying Frontend Metrics via Cypress

To verify that frontend metrics are correctly sent to the OTel Collector, run the Cypress E2E tests:

```bash
cd frontend
npm run cypress:run
```

The test will:
1. Navigate to the frontend application
2. Wait for metrics to be exported
3. Query the OTel Collector's Prometheus endpoint to verify the `document_load_duration_seconds` metric is present

### Troubleshooting

- **Metric not found**: Check the `/metrics` endpoint directly at `http://localhost:8000/metrics` to see the actual metric names exposed by the application.
- **No metrics at all**: Ensure the `fastapi-backend` target is `UP` in Prometheus Targets page. Verify the `PrometheusPipeline` is enabled in OTel Collector if using OTel-collected metrics.

## 2. Verify Traces in Tempo/Jaeger

### Steps

1. **Open Grafana**: Navigate to `http://localhost:3000`.
2. **Explore with Tempo**:
   - Go to the `Explore` view.
   - Select the `Tempo` or `Jaeger` datasource from the dropdown.
   - Click `Run Query` or use the search to find traces.
3. **Query for traces**: Use the search `backend-service` or `{resource.service.name="backend-service"}` to find traces.
4. **Expected Result**: You should see a list of recent traces. Clicking on a trace should display its full span hierarchy, including spans from both the frontend and backend.

### Troubleshooting

- **No traces**: Ensure the `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable is set on the backend to point to the OTel Collector (`http://otel-collector:4318`).
- Verify OTel Collector logs for trace ingestion errors and ensure the Tempo exporter is configured in the traces pipeline.

## 3. Verify Logs in Loki

### Steps
1. ❯ curl -G -s "http://localhost:3100/loki/api/v1/query" --data-urlencode 'query={service_name!=""}'
2. 
3. **Open Grafana**: Navigate to `http://localhost:3000`.
4. **Explore with Loki**:
   - Go to the `Explore` view.
   - Select the `Loki` datasource.
5. **Query for logs**: Use LogQL queries:
    - `{service_name="backend-service"}` - Logs from the backend service
    - `{service_name="otel-collector"}` - OTel Collector logs
6. **Expected Result**: You should see log entries from the corresponding service, enriched with OpenTelemetry context like `trace_id` and `span_id`.

### Troubleshooting

- **No logs**: Ensure the backend is configured to send logs to the OTel Collector. Check the OTel Collector logs for any errors in the Loki exporter. Verify the Loki exporter is enabled in the logs pipeline.

## Troubleshooting

### Common Issues

- **Backend `OTEL_EXPORTER_OTLP_ENDPOINT` not set**: This is the most common cause of missing telemetry. Add `- OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318` to the backend service environment in `docker-compose.yml` or `docker-compose.override.yml`.
- **Frontend metrics not enabled**: Ensure `VITE_OTEL_METRICS_ENABLED=true` is set in the frontend service environment in `docker-compose.yml`. Also verify `VITE_OTEL_COLLECTOR_METRICS_URL` points to the OTel Collector metrics endpoint.
- **Wrong metric names**: 
  - Backend: Run `curl http://localhost:8000/metrics` to see the actual metrics exposed by the application.
  - Frontend: Run `curl http://localhost:8889/metrics` to see all metrics received by the OTel Collector.
- **Service name mismatch**: The OpenTelemetry resource attribute `service.name` is used as the label name in Loki (e.g., `{service_name="backend-service"}`). For frontend, the service name should be `frontend-service`.

### Checking OTel Collector Logs

To diagnose pipeline issues, check the OTel Collector logs:

```bash
podman-compose -f docker-compose.yml -f docker-compose.override.yml logs otel-collector
```

Look for:
- `TracesExporter` output confirming traces are exported
- `MetricsExporter` output confirming metrics are exported (including frontend metrics)
- Any errors related to Tempo (`tempo:4317`), Loki (`http://loki:3100`), or Prometheus endpoints