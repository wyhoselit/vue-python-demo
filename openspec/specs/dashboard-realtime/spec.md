# Dashboard Real-time Metrics

## Problem Statement

The dashboard frontend requires real-time metrics data to display live API request trends, response time distributions, status code breakdowns, and active user counts. The backend was missing a `/realtime` endpoint, had incorrect module imports causing runtime errors, and returned field names in snake_case format while the frontend expected camelCase. These issues caused the dashboard to fail loading with `AttributeError: 'builtin_function_or_method' object has no attribute 'randint'` and `-Infinity` SVG parsing errors when ApexCharts received NaN values from malformed responses.

## Solution

Implement a `GET /api/v1/dashboard/realtime` endpoint that returns an array of real-time metrics data points. Each data point contains API request counts, average response times, HTTP status code distributions, and active user counts. Fix the Python import statement to correctly access the `random` module's `randint` and `uniform` functions. Ensure all response field names use camelCase naming convention to match frontend TypeScript interfaces.

## User Stories

1. As a dashboard user, I want to see live API request counts, so that I can monitor system load in real-time.
2. As a dashboard user, I want to view current average response times, so that I can assess API performance.
3. As a dashboard user, I want to see HTTP status code distributions (2xx, 4xx, 5xx), so that I can identify error rates.
4. As a dashboard user, I want to observe active user counts, so that I can track user engagement.
5. As a dashboard user, I want data updated every 5 seconds, so that I have fresh metrics without manual refresh.
6. As a frontend developer, I want camelCase field names in the API response, so that the data maps directly to TypeScript interfaces.
7. As a system administrator, I want consistent API response types, so that frontend components can render charts without NaN errors.
8. As a dashboard user, I want a fallback to mock data when the API fails, so that the dashboard remains usable during outages.
9. As a project maintainer, I want working endpoints with correct imports, so that the backend starts without runtime errors.

## Implementation Decisions

### API Endpoint
- Created `GET /dashboard/realtime` route at `backend/app/modules/dashboard/api/dashboard.py`
- Returns `list[RealtimeDataPoint]` with single data point per response
- Uses Python `random` module to generate realistic sample metrics

### Response Model
- `timestamp`: ISO 8601 formatted string from `datetime.now().isoformat()`
- `requests`: Integer count of API requests (0-1000 range)
- `avgResponseTime`: Float average response time in milliseconds (0-100ms range)
- `status2xx`: Integer count of successful responses (0-100 range)
- `status4xx`: Integer count of client errors (0-100 range)  
- `status5xx`: Integer count of server errors (0-100 range)
- `activeUsers`: Integer count of connected users (0-100 range)

### Field Naming Convention
- Chose camelCase for response fields to match:
  - Frontend TypeScript interface `RealtimeDataPoint`
  - ApexCharts data mappings in computed properties
  - Existing API conventions in the codebase

### Import Fix
- Changed `from random import random` → `import random` to enable access to `random.randint()` and `random.uniform()`
- Avoids shadowing Python builtin `random` function from the `random` module

### Data Generation Strategy
- Use random values for prototyping/demo purposes
- Values generated within realistic ranges for dashboard visualization
- Single data point returned per call (frontend handles array of points)

## Testing Decisions

### Backend Tests (Backend)
- Location: `backend/app/modules/dashboard/__tests__/dashboard.test.py` (or similar)
- Test that endpoint returns HTTP 200 with valid JSON array
- Test response structure matches `RealtimeDataPoint` schema
- Test field names are camelCase
- Test values are within expected ranges

### Frontend Tests (Frontend)  
- Location: `frontend/src/modules/dashboard/__tests__/Dashboard.test.ts`
- Test that `fetchRealtimeData` correctly maps API response to component state
- Test that charts render without NaN/Infinity errors
- Test that realtime interval updates data correctly
- Test fallback to mock data when API fails

### Prior Art
- Follows existing `get_dashboard_stats()` endpoint pattern
- Uses same Vuetify chart component patterns as existing dashboard
- Error handling matches established `fetchData()` pattern with fallback

## Out of Scope

- Actual database metrics collection (currently returns random values)
- Historical data history (single point per request)
- Authentication/authorization for the endpoint
- Rate limiting or request throttling
- WebSocket-based real-time streaming (uses HTTP polling)
- Integration with actual PostgreSQL or Redis metrics

## Further Notes

The current implementation uses `random` module for generating sample metrics. For production use, this should be replaced with actual metrics from:
- Application metrics library (Prometheus, OpenTelemetry metrics)
- Database query counts
- Active session tracking
- HTTP middleware for status code counting

The frontend polling interval is currently 5 seconds (`5000ms`). This may need adjustment based on actual performance requirements.