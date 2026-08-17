## Context

The current frontend application (`frontend/src/modules/core/observability.ts`) sets up OpenTelemetry for tracing and logging, with optional metrics support. The metrics pipeline is configured to export via OTLP HTTP to the OTel Collector (`otel-collector:4318/v1/metrics`), which then exposes a Prometheus endpoint on port 8889. Prometheus is configured to scrape this endpoint.

However, the frontend codebase currently lacks explicit metric instrumentation (counters, histograms, etc.) for user interactions or performance measurements. The `PeriodicExportingMetricReader` is configured but no custom meters or instruments are created, resulting in no application-specific metrics being sent.

## Goals / Non-Goals

**Goals:**
- Add explicit OpenTelemetry metric instruments (counters, histograms) for:
  - User interactions: page views, button clicks, form submissions, route changes
  - Performance: component render times, API call latencies
- Ensure metrics are correctly exported through the existing OTel Collector → Prometheus pipeline
- Provide a reusable pattern for adding metrics to any Vue component or composable
- Verify end-to-end flow: frontend instrumentation → OTel Collector → Prometheus → Grafana

**Non-Goals:**
- Redesigning the OTel Collector or Prometheus configuration (currently functional)
- Implementing custom Grafana dashboards (out of scope, but visualization is the end goal)
- Backend metric instrumentation (already exists)

## Decisions

**Decision 1: Metric Instrumentation Approach**
- **Choice**: Use the global `MeterProvider` set in `observability.ts` via `metrics.setGlobalMeterProvider(meterProvider)`. Create a dedicated meter (`getMeter('frontend-app')`) in a `frontend/src/modules/core/metrics/metrics.ts` utility to be used across the application.
- **Rationale**: Leverages existing OTel setup. Centralizes meter creation, ensuring consistent resource attributes (service.name). Avoids creating multiple `MeterProvider` instances.

**Decision 2: Metric Types & Naming Convention**
- **Choice**: Use semantic conventions where applicable (e.g., `http.client.request.duration` for API calls). For custom app metrics, prefix with `frontend.app.` (e.g., `frontend.app.page_view`, `frontend.app.button_click`, `frontend.app.component_render_duration`).
- **Rationale**: Aligns with OpenTelemetry Semantic Conventions for interoperability. Prefix avoids collisions and clearly identifies frontend-originated metrics.

**Decision 3: Instrumentation Integration Points**
- **Page Views**: Instrument Vue Router's `afterEach` navigation guard.
- **User Interactions (Clicks/Submits)**: Create a composable `useMetrics()` providing helper functions (`trackClick`, `trackFormSubmit`) that components can call. Alternatively, use a global directive or event listener for automatic click tracking (more invasive, less context). Composable approach chosen for explicit, contextual tracking.
- **Performance (Component Render)**: Use Vue's `onBeforeMount` / `onMounted` lifecycle hooks with `performance.now()` wrapped in a helper, or a custom directive. Helper function approach chosen for simplicity and explicitness.
- **API Call Latency**: Wrap the existing `useApi` composable (`frontend/src/shared/useApi.ts`) to record duration of `get`, `post`, `put`, `delete` calls using a histogram.

**Decision 4: Attributes (Labels)**
- **Standard Attributes**: `service.name` (from Resource), `service.instance.id` (if available).
- **Custom Attributes**:
  - Page Views: `route.name`, `route.path`
  - Clicks: `element_id`, `element_type`, `page_route`
  - API Calls: `http.method`, `http.url`, `http.status_code`, `error.type` (if failed)
  - Component Render: `component_name`

## Risks / Trade-offs

- **Risk: High Cardinality Attributes** → Mitigation: Avoid high-cardinality values (e.g., full URLs with query params, user IDs) as metric attributes. Use normalized route names/paths. Limit attribute values to known enums where possible.
- **Risk: Performance Overhead** → Mitigation: OpenTelemetry JS metrics SDK is designed for low overhead. Batching (`PeriodicExportingMetricReader` at 1s) reduces network calls. Ensure histogram boundaries are reasonable.
- **Risk: Missing Metrics in Pipeline** → Mitigation: Implement verification steps (check OTel Collector `/metrics` endpoint, Prometheus targets UI, query Prometheus directly) as part of the implementation tasks.
- **Trade-off: Explicit vs. Automatic Instrumentation** → Explicit (composables/hooks) chosen over automatic (global listeners) for richer context (attributes) and lower noise, at the cost of developer effort to instrument.

## Grafana Dashboard Update

- **Action**: Updated `dockerdata/observability/grafana/provisioning/dashboards/frontend-observability.json` to include panels for `frontend.app.page_view` and adjusted existing panels to reflect new frontend metrics.