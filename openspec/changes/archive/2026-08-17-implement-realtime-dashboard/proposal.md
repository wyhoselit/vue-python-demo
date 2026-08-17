## Why

The existing dashboard in the Vue.js frontend only displayed static statistics and a user table. To provide meaningful operational insights, we need a real-time dashboard with live data visualization showing API request trends, response time distributions, status code breakdowns, and active user metrics — enabling teams to monitor system health at a glance.

## What Changes

- Added Vue ApexCharts library for real-time charting
- Created reusable `ApexChart` component for consistent chart rendering
- Enhanced `Dashboard.vue` with four real-time charts:
  - API Request Trends (area chart)
  - Response Time Distribution (line chart)
  - Status Code Distribution (donut chart)
  - Active Users Trend (bar chart)
- Implemented automatic data refresh every 5 seconds with mock data fallback
- Added proper cleanup of intervals on component unmount
- Updated observability instrumentation (router, axios, pinia) to use OpenTelemetry without deprecated Sentry APIs
- Added comprehensive test coverage for new dashboard functionality

## Capabilities

### New Capabilities
- `realtime-dashboard`: Real-time data visualization dashboard with live-updating charts
- `charting-library-integration`: Vue 3 integration with ApexCharts via vue3-apexcharts

### Modified Capabilities
- `dashboard-stats`: Extended existing dashboard statistics to include real-time metrics
- `observability-instrumentation`: Updated router, axios, and pinia instrumentation to use modern OpenTelemetry APIs

## Impact

### Frontend Code
- `frontend/src/main.ts`: Register Vue ApexCharts globally
- `frontend/src/modules/shared/components/ApexChart.vue`: New reusable chart component
- `frontend/src/modules/dashboard/views/Dashboard.vue`: Enhanced with four real-time charts
- `frontend/src/modules/core/observability.ts`: Removed deprecated Sentry configuration
- `frontend/src/modules/core/router-observability.ts`: Simplified to use OpenTelemetry only
- `frontend/src/plugins/router-instrumentation.ts`: Removed Sentry, use OpenTelemetry spans
- `frontend/src/modules/dashboard/__tests__/Dashboard.test.ts`: Updated tests for new charts and real-time updates

### Dependencies
- Added `apexcharts` and `vue3-apexcharts` npm packages

### Testing
- All existing tests pass (59 tests)
- New test added for cleanup of real-time update intervals on unmount