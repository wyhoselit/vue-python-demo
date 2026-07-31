## ADDED Requirements

### Requirement: Dashboard stats endpoint
The system SHALL provide a `GET /api/v1/dashboard/stats` endpoint that returns platform statistics.

#### Scenario: Stats endpoint returns correct structure
- **WHEN** client sends `GET /api/v1/dashboard/stats`
- **THEN** response SHALL have status 200
- **AND** body SHALL contain `total_users` (integer)
- **AND** body SHALL contain `active_sessions` (integer)
- **AND** body SHALL contain `api_calls_24h` (integer)

### Requirement: Users list endpoint
The system SHALL provide a `GET /api/v1/users` endpoint that returns a list of users.

#### Scenario: Users endpoint returns array
- **WHEN** client sends `GET /api/v1/users`
- **THEN** response SHALL have status 200
- **AND** body SHALL be an array of user objects
- **AND** each user SHALL have `id` (integer), `name` (string), `email` (string), `status` (string)

### Requirement: Router registration
The system SHALL register the new endpoints in the v1 API router.

#### Scenario: Dashboard router included
- **WHEN** application starts
- **THEN** `dashboard.router` SHALL be included in `api_router` with prefix `/dashboard`

#### Scenario: Users router included
- **WHEN** application starts
- **THEN** `users.router` SHALL be included in `api_router` with prefix `/users`