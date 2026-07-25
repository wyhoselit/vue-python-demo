# Backend Error Handling Specification

## Purpose
Defines global exception handlers for consistent JSON error responses across the API.

## Requirements

### Requirement: HTTPException handler
The system SHALL catch all `HTTPException` instances and return formatted JSON responses.

#### Scenario: HTTPException returns JSON
- **WHEN** an endpoint raises `HTTPException(status_code=404, detail="Not found")`
- **THEN** response SHALL be:
  - Status code: 404
  - Body: `{"detail": "Not found"}`

#### Scenario: Different status codes handled
- **WHEN** `HTTPException` with status 400, 401, 403, 404, 422, 500 is raised
- **THEN** response SHALL have matching status code and JSON body with `detail` field.

### Requirement: Generic exception handler
The system SHALL catch all unhandled exceptions and return a 500 error.

#### Scenario: Unhandled exception returns 500
- **WHEN** an endpoint raises an unexpected `Exception`
- **THEN** response SHALL be:
  - Status code: 500
  - Body: `{"detail": "Internal server error"}`

### Requirement: Validation error handling
The system SHALL return 422 for Pydantic validation errors (automatic FastAPI behavior).

#### Scenario: Invalid request body
- **WHEN** request body fails Pydantic validation
- **THEN** response SHALL be:
  - Status code: 422
  - Body: JSON with validation error details

### Requirement: Consistent error response format
All error responses SHALL follow a consistent JSON format with a `detail` field.

#### Scenario: Error format consistency
- **WHEN** any error occurs (HTTPException, validation, generic)
- **THEN** response SHALL include `detail` field with error message.

### Requirement: Error handling tests
The system SHALL include tests for exception handlers.

#### Scenario: 404 error test
- **WHEN** `test_404_error` requests non-existent endpoint
- **THEN** response SHALL be 404 with `{"detail": "Not found"}`.

#### Scenario: 400 error test
- **WHEN** `test_400_error` triggers bad request
- **THEN** response SHALL be 400 with `{"detail": "Bad request"}`.

#### Scenario: 500 error test
- **WHEN** `test_500_error` triggers unhandled exception
- **THEN** response SHALL be 500 with `{"detail": "Internal server error"}`.