## Purpose

This capability defines global exception handling and error response formatting for the FastAPI backend.

## Requirements

### Requirement: Global exception handler for HTTPException
The system SHALL catch all HTTPException instances and return formatted JSON responses.

#### Scenario: 404 error returns JSON
- **WHEN** endpoint raises HTTPException with status 404
- **THEN** system SHALL return JSON response with error details

#### Scenario: 400 error returns JSON
- **WHEN** endpoint raises HTTPException with status 400
- **THEN** system SHALL return JSON response with error details

### Requirement: Global exception handler for unhandled exceptions
The system SHALL catch all unhandled exceptions and return a 500 error.

#### Scenario: Unhandled exception returns 500
- **WHEN** endpoint raises an unexpected exception
- **THEN** system SHALL return 500 status with generic error message

#### Scenario: Error logged
- **WHEN** unhandled exception occurs
- **THEN** system SHALL log the exception details

### Requirement: Consistent error response format
The system SHALL return errors in a consistent JSON format.

#### Scenario: Error response structure
- **WHEN** any error occurs
- **THEN** response SHALL include `detail` field with error message

### Requirement: Validation errors handled
The system SHALL return 422 for Pydantic validation errors.

#### Scenario: Invalid request body
- **WHEN** request body fails Pydantic validation
- **THEN** system SHALL return 422 status with validation error details