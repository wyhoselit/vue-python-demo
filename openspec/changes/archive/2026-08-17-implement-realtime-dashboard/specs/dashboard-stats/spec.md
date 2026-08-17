## MODIFIED Requirements

### Requirement: Dashboard Statistics Display
The dashboard SHALL display key operational statistics for total users, active sessions, and API calls within the last 24 hours.

#### Scenario: Display static statistics
- **WHEN** the dashboard is loaded
- **THEN** the system SHALL fetch and display the current values for total users, active sessions, and API calls (24h) in dedicated cards.

### Requirement: User List Display
The dashboard SHALL display a paginated table of registered users.

#### Scenario: Display user data in a table
- **WHEN** the dashboard is loaded
- **THEN** the system SHALL fetch and display a list of users in a data table with columns for ID, Name, Email, and Status.
- **THEN** the user table SHALL be paginated with 10 items per page.