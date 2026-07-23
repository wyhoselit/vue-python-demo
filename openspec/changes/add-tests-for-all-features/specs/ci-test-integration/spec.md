## ADDED Requirements

### Requirement: Backend tests can be run in CI
The system SHALL provide a single command to execute all backend tests for CI/CD.

#### Scenario: Backend CI command executes tests
- **WHEN** `pytest` command is run (e.g., in a CI pipeline)
- **THEN** all backend tests SHALL be discovered and executed.
- **AND** the command SHALL return a non-zero exit code on test failure.

### Requirement: Frontend tests can be run in CI
The system SHALL provide a single command to execute all frontend tests for CI/CD.

#### Scenario: Frontend CI command executes tests
- **WHEN** `npm run test` (or similar) is run (e.g., in a CI pipeline)
- **THEN** all frontend tests SHALL be discovered and executed.
- **AND** the command SHALL return a non-zero exit code on test failure.

### Requirement: CI script runs both backend and frontend tests
The system SHALL provide a script or command to run all tests (backend and frontend) for the entire project.

#### Scenario: Combined CI command executes all tests
- **WHEN** `npm test:ci` (or similar) is run from the project root
- **THEN** both backend and frontend tests SHALL be executed sequentially or in parallel.
- **AND** the command SHALL return a non-zero exit code if any test fails.
