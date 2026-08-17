## ADDED Requirements

### Requirement: Frontend Performance Metrics Collection
The frontend application SHALL collect and export OpenTelemetry metrics for application performance.

#### Scenario: API Call Latency Metric
- **WHEN** an API call is made via the `useApi` composable
- **THEN** a histogram metric `http.client.duration` SHALL be recorded with attributes `http.method`, `http.url` (templated/generalized), and `http.status_code`.

#### Scenario: Component Render Duration Metric
- **WHEN** a component is mounted and rendered
- **THEN** a histogram metric `frontend.app.component_render_duration` SHALL be recorded with attributes `component_name` and `route.path`.
