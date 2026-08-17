## 1. Dependencies & Setup

- [x] 1.1 Install `apexcharts` and `vue3-apexcharts` npm packages
- [x] 1.2 Register Vue ApexCharts globally in `main.ts`

## 2. Chart Component

- [x] 2.1 Create reusable `ApexChart.vue` wrapper component
- [x] 2.2 Implement chart lifecycle (mount, updateSeries, updateOptions, destroy)
- [x] 2.3 Add TypeScript types for series and chartOptions props
- [x] 2.4 Handle reactive updates via watchers

## 3. Dashboard Enhancement

- [x] 3.1 Add four chart components to Dashboard.vue layout
  - [x] 3.1.1 API Request Trends (area chart)
  - [x] 3.1.2 Response Time Distribution (line chart)
  - [x] 3.1.3 Status Code Distribution (donut chart)
  - [x] 3.1.4 Active Users Trend (bar chart)
- [x] 3.2 Define TypeScript interfaces for real-time data points
- [x] 3.3 Implement computed properties for chart series and options
- [x] 3.4 Add real-time data fetching with `/dashboard/realtime` endpoint
- [x] 3.5 Implement mock data fallback when API unavailable
- [x] 3.6 Add 5-second polling interval for real-time updates
- [x] 3.7 Implement cleanup of interval on component unmount

## 4. Observability Cleanup

- [x] 4.1 Remove deprecated Sentry imports and initialization from `observability.ts`
- [x] 4.2 Update `router-observability.ts` to use only OpenTelemetry
- [x] 4.3 Update `router-instrumentation.ts` to use only OpenTelemetry
- [x] 4.4 Fix TypeScript errors in observability modules

## 5. Testing

- [x] 5.1 Update existing Dashboard tests for new chart components
- [x] 5.2 Add test for real-time interval cleanup on unmount
- [x] 5.3 Verify all 59 tests pass
- [x] 5.4 Run typecheck and fix all TypeScript errors

## 6. Documentation

- [x] 6.1 Create proposal.md
- [x] 6.2 Create design.md
- [x] 6.3 Create specs for realtime-dashboard capability
- [x] 6.4 Create specs for charting-library-integration capability
- [x] 6.5 Create specs for dashboard-stats capability (modified)
- [x] 6.6 Create specs for observability-instrumentation capability (modified)
- [x] 6.7 Create tasks.md