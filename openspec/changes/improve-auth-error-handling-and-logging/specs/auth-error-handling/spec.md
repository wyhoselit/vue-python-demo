# ADDED Requirements

## Requirement: Structured Logging (Backend)
The system SHALL implement structured JSON logging for authentication operations.

### Scenario: Registration attempt
- **WHEN** a client attempts registration
- **THEN** log entry includes: event type, email, success/failure, error_code, timestamp, request_id

### Scenario: Login attempt
- **WHEN** a client attempts login
- **THEN** log entry includes: event type, email, success/failure, error_code, timestamp, request_id

## Requirement: Custom Exception Types (Backend)
The system SHALL define custom exception classes for auth errors.

### Exception Types
- **EmailAlreadyExistsError**: 409 Conflict, code `EMAIL_ALREADY_EXISTS`
- **InvalidCredentialsError**: 401 Unauthorized, code `INVALID_CREDENTIALS`
- **ValidationError**: 422 Unprocessable, code `VALIDATION_ERROR`

## Requirement: Unified Error Response Format (Backend)
All auth endpoints SHALL return errors in consistent format.

### Error Response Schema
```json
{
  "detail": "Human-readable message",
  "error_code": "MACHINE_READABLE_CODE"
}
```

(Note: `request_id` is returned in the response header `X-Request-ID`.)

## Requirement: Frontend Error Display
The frontend SHALL surface specific error messages to users.

### Scenario: Email exists on register
- **WHEN** backend returns `EMAIL_ALREADY_EXISTS`
- **THEN** show "This email is already registered"

### Scenario: Invalid login
- **WHEN** backend returns `INVALID_CREDENTIALS`
- **THEN** show "Incorrect email or password"

## MODIFIED Requirements

### Requirement: Auth Endpoints (from add-user-authentication)
- Modified: Register and login endpoints now return structured errors.