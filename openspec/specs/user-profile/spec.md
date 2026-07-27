# user-profile Specification

## Purpose
TBD - created by archiving change add-users-me-endpoint. Update Purpose after archive.
## Requirements
### Requirement: Get Current User Profile
The system SHALL provide an authenticated endpoint to retrieve the current user's profile.

#### Scenario: Authenticated user retrieves profile
- **WHEN** an authenticated user sends GET request to `/api/v1/users/me` with valid JWT cookie
- **THEN** the system responds with 200 OK and JSON containing `id` and `email`

#### Scenario: Unauthenticated request denied
- **WHEN** a request to `/api/v1/users/me` lacks valid JWT cookie
- **THEN** the system responds with 401 Unauthorized and error code `INVALID_CREDENTIALS`

#### Scenario: Expired token rejected
- **WHEN** a request includes an expired JWT cookie
- **THEN** the system responds with 401 Unauthorized and error code `TOKEN_EXPIRED`

#### Scenario: User deleted but token valid
- **WHEN** JWT references a user that no longer exists in database
- **THEN** the system responds with 401 Unauthorized

