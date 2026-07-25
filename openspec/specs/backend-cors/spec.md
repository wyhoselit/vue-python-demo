# Backend CORS Middleware Specification

## Purpose
Defines the CORS (Cross-Origin Resource Sharing) configuration for frontend-backend communication.

## Requirements

### Requirement: CORSMiddleware added to FastAPI application
The system SHALL add `CORSMiddleware` to the FastAPI application during initialization.

#### Scenario: Middleware configured in main.py
- **WHEN** `main.py` creates the `FastAPI` app
- **THEN** it SHALL call `app.add_middleware(CORSMiddleware, ...)` with appropriate configuration.

### Requirement: Allowed origins from configuration
The system SHALL use `settings.CORS_ORIGINS` to configure allowed origins.

#### Scenario: CORS_ORIGINS parsed correctly
- **WHEN** `settings.CORS_ORIGINS` is `"http://localhost:5173,http://localhost:3000"`
- **THEN** `allow_origins` SHALL be `["http://localhost:5173", "http://localhost:3000"]`.

#### Scenario: Default origin includes frontend dev server
- **WHEN** no `.env` file is present
- **THEN** `allow_origins` SHALL include `"http://localhost:5173"`.

### Requirement: Credentials allowed
The system SHALL allow credentials (cookies, authorization headers) in CORS requests.

#### Scenario: `allow_credentials=True`
- **WHEN** CORS middleware is configured
- **THEN** `allow_credentials` SHALL be `True`.

### Requirement: Standard HTTP methods allowed
The system SHALL allow all standard HTTP methods for CORS requests.

#### Scenario: `allow_methods=["*"]`
- **WHEN** CORS middleware is configured
- **THEN** `allow_methods` SHALL be `["*"]`.

### Requirement: Standard headers allowed
The system SHALL allow all headers for CORS requests.

#### Scenario: `allow_headers=["*"]`
- **WHEN** CORS middleware is configured
- **THEN** `allow_headers` SHALL be `["*"]`.

### Requirement: CORS test
The system SHALL include a test for CORS headers.

#### Scenario: OPTIONS request from allowed origin
- **WHEN** `test_api_cors` runs an OPTIONS request from `http://localhost:5173`
- **THEN** response SHALL include:
  - `Access-Control-Allow-Origin: http://localhost:5173`
  - `Access-Control-Allow-Methods: *`
  - `Access-Control-Allow-Headers: *`
  - `Access-Control-Allow-Credentials: true`

#### Scenario: OPTIONS request from disallowed origin
- **WHEN** OPTIONS request from `http://evil.com`
- **THEN** response SHALL NOT include `Access-Control-Allow-Origin: http://evil.com`.