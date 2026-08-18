# 01 — Add Dashboard Realtime API Endpoint

## What to build
Dashboard displays live API request trends, response times, status codes, and active users through a working backend endpoint that frontend can poll.

## Acceptance criteria
- [ ] `GET /api/v1/dashboard/realtime` endpoint exists and returns HTTP 200
- [ ] Response is JSON array with `timestamp`, `requests`, `avgResponseTime`, `status2xx`, `status4xx`, `status5xx`, `activeUsers` fields
- [ ] Endpoint registered in the v1 API router

## Blocked by
None — can start immediately