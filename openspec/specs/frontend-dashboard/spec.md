# Frontend Dashboard Page Specification

## Purpose
Defines the Dashboard view with real API integration, loading/error states, and Vuetify data presentation.

## Requirements

### Requirement: Dashboard view component
The system SHALL provide a `Dashboard` view component at `frontend/src/views/Dashboard.vue`.

#### Scenario: Dashboard renders within layout
- **WHEN** user navigates to root path "/"
- **THEN** `Dashboard.vue` SHALL be rendered inside `DefaultLayout`'s `<router-view />`.

### Requirement: Real API data integration
The Dashboard SHALL fetch and display real data from backend API endpoints.

#### Scenario: Fetch dashboard stats on mount
- **WHEN** Dashboard component mounts
- **THEN** it SHALL call `GET /api/v1/dashboard/stats` via `useApi` composable.

#### Scenario: Fetch users list on mount
- **WHEN** Dashboard component mounts
- **THEN** it SHALL call `GET /api/v1/users` via `useApi` composable.

### Requirement: Loading state
The Dashboard SHALL display a loading indicator while data is being fetched.

#### Scenario: Loading indicator visible
- **WHEN** API requests are in progress
- **THEN** a `v-progress-circular` or similar loading indicator SHALL be visible.

#### Scenario: Loading indicator hidden after fetch
- **WHEN** API requests complete (success or error)
- **THEN** loading indicator SHALL be hidden.

### Requirement: Error state handling
The Dashboard SHALL handle and display API errors gracefully.

#### Scenario: Error message displayed
- **WHEN** API request fails (network error, 4xx, 5xx)
- **THEN** an error message SHALL be displayed using `v-alert` with type "error".

#### Scenario: Error dismissed
- **WHEN** user clicks dismiss on error alert
- **THEN** error message SHALL be hidden.

### Requirement: Metric cards with real data
The Dashboard SHALL display three metric cards with real values from API.

#### Scenario: Total Users card
- **WHEN** stats API returns `total_users: 42`
- **THEN** "Total Users" card SHALL display value "42".

#### Scenario: Active Sessions card
- **WHEN** stats API returns `active_sessions: 15`
- **THEN** "Active Sessions" card SHALL display value "15".

#### Scenario: API Calls card
- **WHEN** stats API returns `api_calls_24h: 1234`
- **THEN** "API Calls (24h)" card SHALL display value "1,234" (formatted).

### Requirement: Data table with users
The Dashboard SHALL display a Vuetify data table with user data.

#### Scenario: User table populated
- **WHEN** users API returns `[{id: 1, name: "John", email: "john@example.com", status: "active"}]`
- **THEN** `v-data-table` SHALL display rows with columns: ID, Name, Email, Status.

#### Scenario: Table headers defined
- **WHEN** table renders
- **THEN** headers SHALL be: ID, Name, Email, Status.

### Requirement: Responsive design
The Dashboard SHALL adapt to different screen sizes.

#### Scenario: Mobile layout
- **WHEN** viewport is mobile (cols="12" md="4")
- **THEN** metric cards SHALL stack in single column.

#### Scenario: Desktop layout
- **WHEN** viewport is desktop
- **THEN** metric cards SHALL display in 3-column grid.

### Requirement: Dashboard tests
The system SHALL include tests for Dashboard component.

#### Scenario: Dashboard renders correctly
- **WHEN** `Dashboard.test.ts` runs
- **THEN** it SHALL verify component renders without errors.

#### Scenario: Dashboard mocks API calls
- **WHEN** test runs with mocked `useApi`
- **THEN** it SHALL verify loading state, success state, and error state handling.