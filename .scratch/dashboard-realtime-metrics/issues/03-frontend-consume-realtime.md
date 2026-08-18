# 03 — Frontend Consumes Realtime Endpoint

## What to build
Dashboard polls `/api/v1/dashboard/realtime` every 5 seconds and updates charts with live data.

## Acceptance criteria
- [ ] `fetchRealtimeData` calls `GET /dashboard/realtime` via `useApi`
- [ ] Data maps correctly to `RealtimeDataPoint` TypeScript interface
- [ ] Charts update without `NaN` or `-Infinity` SVG errors
- [ ] Fallback to mock data when API fails
- [ ] 5-second polling interval via `setInterval`

## Blocked by
- 01 — Add Dashboard Realtime API Endpoint
- 02 — Fix Python Random Module Import