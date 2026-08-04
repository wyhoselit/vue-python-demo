## ADDED Requirements

### Requirement: Bearer token authentication
The system SHALL support `Authorization: Bearer <token>` header authentication for system configuration API endpoints.

### Requirement: Default Bearer Token Initialization
The system SHALL read the default bearer token from a `.token` file during database initialization/migration.
- If `.token` exists, its content SHALL be used to set `system.default_bearer_token` in the database.
- If `.token` does not exist or is empty, `system.default_bearer_token` remains empty.

#### Scenario: Successful GET request with Bearer token
- **WHEN** user sends GET request to `/api/v1/system/config/system.tracing` with valid Bearer token
- **THEN** system returns 200 OK with config value

#### Scenario: Successful PUT request with Bearer token
- **WHEN** user sends PUT request to `/api/v1/system/config/system.tracing` with valid Bearer token and JSON body
- **THEN** system updates config value and returns 200 OK

#### Scenario: Unauthenticated request with Bearer token
- **WHEN** user sends request with invalid Bearer token
- **THEN** system returns 401 Unauthorized

#### Scenario: Request without token
- **WHEN** user sends request with neither cookie nor Bearer token
- **THEN** system returns 401 Unauthorized

#### Scenario: System initialization with .token file
- **WHEN** database migration runs and `.token` file contains `my-secret-token`
- **THEN** `system.default_bearer_token` in database is set to `my-secret-token`
