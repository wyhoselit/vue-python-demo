## Context

The Vue.js frontend had a basic dashboard displaying static statistics (total users, active sessions, API calls) and a user table. The requirement was to add real-time data visualization capabilities to monitor system health dynamically.

Current state before this change:
- Dashboard.vue: Static stats cards + user table only
- No charting library integrated
- Observability used mixed Sentry + OpenTelemetry with some deprecated APIs
- No real-time data fetching or automatic refresh

## Goals / Non-Goals

**Goals:**
- Add real-time charting to dashboard with 4 chart types (area, line, donut, bar)
- Use ApexCharts via vue3-apexcharts for Vue 3 Composition API compatibility
- Create reusable ApexChart component for consistent chart rendering
- Implement 5-second auto-refresh with mock data fallback
- Clean up OpenTelemetry instrumentation (remove deprecated Sentry code)
- Maintain all existing test coverage (59 tests passing)

**Non-Goals:**
- Backend API changes (mock data used for real-time endpoints)
- WebSocket implementation (polling-based approach used)
- Historical data persistence
- User-customizable dashboards
- Alerting or threshold notifications

## Decisions

### 1. Charting Library: ApexCharts via vue3-apexcharts

**Rationale:** Research showed Vue ApexCharts provides excellent Vue 3 Composition API support, full TypeScript support, reactive updates out-of-the-box, and rich chart types. Alternatives considered:
- Vue ECharts: More powerful but heavier bundle, steeper learning curve
- Vue Chart.js: Simpler but fewer advanced features, reactivity gotchas

**Trade-off:** ApexCharts has larger bundle size (~200KB) but provides all needed chart types without configuration complexity.

### 2. Component Architecture: Reusable ApexChart Wrapper

**Rationale:** Created `ApexChart.vue` as a thin wrapper around ApexCharts instance to:
- Encapsulate chart lifecycle (mount, update, destroy)
- Provide consistent props interface (title, chartId, series, chartOptions)
- Handle reactive updates via watchers on series and options
- Allow easy swapping of charting library in future

**Alternative considered:** Direct ApexCharts usage in Dashboard.vue — rejected due to code duplication across 4 charts.

### 3. Real-time Data: Polling with Mock Fallback

**Rationale:** 5-second polling interval with `/dashboard/realtime` endpoint. If endpoint fails or returns empty, generates realistic mock data locally. This approach:
- Works without backend changes
- Provides immediate visual feedback
- Simulates real-world data patterns
- Easy to replace with WebSocket later

**Trade-off:** Polling creates more network requests than WebSocket but simpler to implement and debug.

### 4. Observability: Remove Sentry, Use OpenTelemetry Only

**Rationale:** Existing code had mixed Sentry + OpenTelemetry with deprecated Sentry APIs (`startTransaction`, `configureScope`, `endIdleTransaction`). Removed Sentry entirely:
- Simplifies instrumentation
- Reduces bundle size
- Uses vendor-neutral OpenTelemetry
- Avoids license/cost concerns with Sentry

**Migration:** Replaced Sentry transaction/spans with OpenTelemetry tracer spans directly in router and axios instrumentation.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| ApexCharts bundle size impact | Tree-shaking enabled; only import needed chart types |
| Polling creates server load | 5-second interval is reasonable; can increase to 10-30s in production |
| Mock data may mislead users | Clearly labeled as "simulated" in development; replace with real API |
| Chart cleanup on unmount | Interval cleared in `onUnmounted`; verified with test |
| TypeScript errors in observability | Fixed by removing Sentry types and using OpenTelemetry types only |

## Migration Plan

1. **Dependencies**: `npm install apexcharts vue3-apexcharts` ✅
2. **Global Registration**: Add `app.use(VueApexCharts)` in main.ts ✅
3. **Chart Component**: Create `ApexChart.vue` wrapper ✅
4. **Dashboard Enhancement**: Add 4 charts with computed series/options ✅
5. **Real-time Logic**: Implement polling + mock fallback ✅
6. **Observability Cleanup**: Remove Sentry from router/axios/pinia ✅
7. **Tests**: Update Dashboard tests, add unmount cleanup test ✅
8. **Typecheck**: Fix all TypeScript errors ✅
9. **Verify**: All 59 tests pass ✅

**Rollback:** Revert package installs and component changes. No database migrations.

## Open Questions

1. **Production real-time endpoint**: What should `/dashboard/realtime` return? Current mock simulates 20 data points with 30-second intervals.
2. **Chart customization**: Should users be able to configure time ranges, chart types, or refresh intervals?
3. **Performance at scale**: With many concurrent users, polling every 5s may need optimization (WebSocket, SSE, or longer intervals).
4. **Error boundaries**: Should chart errors be caught and displayed gracefully without breaking entire dashboard?