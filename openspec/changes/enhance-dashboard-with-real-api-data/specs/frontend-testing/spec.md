## MODIFIED Requirements

### Requirement: Dashboard component testing with mocks
The system SHALL include tests for Dashboard component that mock API responses.

#### Scenario: Dashboard renders loading state
- **WHEN** test mounts Dashboard with mocked `useApi`
- **THEN** component SHALL show `v-progress-circular` initially

#### Scenario: Dashboard renders success state
- **WHEN** mock returns valid stats and users data
- **THEN** component SHALL display metric cards with correct values
- **AND** component SHALL display user data table with correct rows

#### Scenario: Dashboard renders error state
- **WHEN** mock rejects with error
- **THEN** component SHALL display `v-alert` with error message

### Requirement: useApi composable testing
The system SHALL include tests for `useApi` composable mocking.

#### Scenario: useApi get method works
- **WHEN** test calls `useApi().get('/dashboard/stats')`
- **THEN** it SHALL return mocked data