## 1. OpenTelemetry Metrics Setup

- [x] 1.1 Create `frontend/src/modules/core/metrics/metrics.ts` to get a meter and expose helper functions (`recordPageView`, `recordButtonClick`, `recordFormSubmit`, `recordComponentRender`, `recordApiCall`).
- [x] 1.2 Update `frontend/src/modules/core/observability.ts` to ensure `metrics.setGlobalMeterProvider` is called early and meters are initialized.

## 2. User Interaction Metrics

- [x] 2.1 Integrate page view tracking into Vue Router in `frontend/src/router/index.ts` using `router.afterEach`.
- [x] 2.2 Create a composable `frontend/src/composables/useMetrics.ts` with `recordButtonClick` and `recordFormSubmit` functions.
- [x] 2.3 Apply `recordButtonClick` to a sample button in a Vue component (e.g., login, register).
- [x] 2.4 Apply `recordFormSubmit` to a sample form submission.

## 3. Performance Metrics

- [x] 3.1 Modify `frontend/src/shared/useApi.ts` to wrap API calls with `recordApiCall` histogram instrumentation.
- [x] 3.2 Create a mixin or composable to record component render duration using Vue lifecycle hooks (`onBeforeMount`, `onMounted`). Apply to a sample component.

## 4. Verification and Debugging

- [x] 4.1 Start all Docker services (`docker-compose up`).
- [x] 4.2 Interact with the frontend to trigger newly instrumented metrics.
- [x] 4.3 Verify OTel Collector is receiving metrics using browser developer tools (network tab, check requests to `http://otel-collector:4318/v1/metrics`).
- [x] 4.4 Check OTel Collector's Prometheus endpoint (`http://localhost:8889/metrics`) for the presence of `frontend.app.*` metrics.
- [x] 4.5 Verify Prometheus is scraping metrics by checking its UI targets status.
- [x] 4.6 Query Prometheus for the new metrics (e.g., `frontend_app_page_view_total`).
