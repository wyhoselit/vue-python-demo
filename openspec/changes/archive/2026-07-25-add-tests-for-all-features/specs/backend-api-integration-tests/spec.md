## ADDED Requirements

### Requirement: Health endpoint returns status "ok"
The system SHALL have integration tests to verify the health endpoints.

#### Scenario: GET /health returns "ok"
- **WHEN** a GET request is made to `/health`
- **THEN** the response status code SHALL be 200
- **AND** the response body SHALL be `{"status": "ok"}`.

#### Scenario: GET /api/v1/health returns "ok"
- **WHEN** a GET request is made to `/api/v1/health`
- **THEN** the response status code SHALL be 200
- **AND** the response body SHALL be `{"status": "ok"}`.

### Requirement: CORS headers are present for allowed origins
The system SHALL have integration tests to verify CORS middleware is correctly configured.

#### Scenario: OPTIONS request from allowed origin receives CORS headers
- **WHEN** an OPTIONS request is made from `http://localhost:5173` to `/health`
- **THEN** the response SHALL include `Access-Control-Allow-Origin: http://localhost:5173`
- **AND** the response SHALL include `Access-Control-Allow-Methods: *`
- **AND** the response SHALL include `Access-Control-Allow-Headers: *`
- **AND** the response SHALL include `Access-Control-Allow-Credentials: true`.

#### Scenario: OPTIONS request from disallowed origin does not receive CORS headers
- **WHEN** an OPTIONS request is made from `http://evil.com` to `/health`
- **THEN** the response SHALL NOT include `Access-Control-Allow-Origin: http://evil.com`.

### Requirement: Global exception handlers function correctly
The system SHALL have integration tests for global exception handling.

#### Scenario: HTTPException returns custom JSON response
- **WHEN** an endpoint raises `HTTPException(404, detail="Item not found")`
- **THEN** the response status code SHALL be 404
- **AND** the response body SHALL be `{"detail": "Item not found"}`.

#### Scenario: Unhandled exception returns 500 error
- **WHEN** an endpoint raises an uncaught generic `Exception`
- **THEN** the response status code SHALL be 500
- **AND** the response body SHALL be `{"detail": "Internal server error"}`.
