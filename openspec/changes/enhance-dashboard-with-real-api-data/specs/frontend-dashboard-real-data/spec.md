## MODIFIED Requirements

### Requirement: Dashboard real API integration
The system SHALL fetch and display real data from backend API endpoints in the Dashboard.

#### Scenario: Dashboard fetches stats on mount
- **WHEN** Dashboard component mounts
- **THEN** it SHALL call `GET /api/v1/dashboard/stats` via `useApi`
- **AND** display `v-progress-circular` while loading
- **AND** update metric cards with real data on success

#### Scenario: Dashboard fetches users on mount
- **WHEN** Dashboard component mounts
- **THEN** it SHALL call `GET /api/v1/users` via `useApi`
- **AND** populate data table with real user data on success

#### Scenario: Dashboard handles API errors
- **WHEN** API calls fail (network error, 4xx, 5xx)
- **THEN** Dashboard SHALL display `v-alert` with error message
- **AND** loading indicator SHALL be hidden

#### Scenario: Metric cards display formatted data
- **WHEN** stats API returns data
- **THEN** "Total Users" card SHALL display `stats.total_users`
- **AND** "Active Sessions" card SHALL display `stats.active_sessions`
- **AND** "API Calls (24h)" card SHALL display formatted `stats.api_calls_24h` (e.g., "15,420")

### Requirement: Frontend API service usage
The system SHALL correctly use the `useApi` composable for API calls.

#### Scenario: useApi configured with correct base URL
- **WHEN** `useApi` is instantiated
- **THEN** it SHALL use `import.meta.env.VITE_API_BASE_URL` or default to `http://localhost:8000/api/v1`

#### Scenario: Axios interceptors handle auth errors
- **WHEN** 401 response is received
- **THEN** interceptor SHALL log unauthorized access error