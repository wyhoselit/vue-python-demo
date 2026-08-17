## Why

Frontend metrics are not currently being collected and reported to Prometheus, making it impossible to monitor the performance and user interaction of the frontend application. This hinders proactive issue detection, performance optimization, and understanding user behavior. Implementing proper metric instrumentation will provide crucial visibility into the frontend's operational health.

## What Changes

- Add client-side metric collection for key user interactions (e.g., button clicks, page views, route changes) and performance data (e.g., component render times).
- Configure OpenTelemetry SDK in the frontend to export these metrics to the OTel Collector.
- Validate the entire metrics pipeline, from frontend instrumentation to Prometheus scraping and Grafana visualization.

## Capabilities

### New Capabilities
- frontend-user-interaction-metrics: Collects metrics related to user interactions (clicks, page views) on the frontend.
- frontend-performance-metrics: Collects metrics related to frontend performance (e.g., component rendering duration, API call timings).

### Modified Capabilities
- <existing-name>: <what requirement is changing>

## Impact

- **Frontend Application**: Requires modifications to integrate OpenTelemetry metrics API and instrument specific components/actions.
- **OpenTelemetry Collector**: Configuration might need adjustments to process new metric types or ensure proper aggregation/export.
- **Prometheus**: Should already be configured to scrape from the OTel Collector, but will receive new metric series.
- **Grafana**: New dashboards or updates to existing ones will be needed to visualize the collected frontend metrics.