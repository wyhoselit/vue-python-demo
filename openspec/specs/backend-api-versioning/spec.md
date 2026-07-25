# Backend API Versioning Specification

## Purpose
Defines the versioned API structure with v1 router, health endpoints, and dashboard statistics endpoints.

## Requirements

### Requirement: API v1 Router
The system SHALL provide an `APIRouter` instance for version 1 endpoints mounted at `/api/v1`.

#### Scenario: Router accessible
- **WHEN** code imports `api_router` from `app.api.router`
- **THEN** it SHALL return the v1 `APIRouter` instance.

#### Scenario: Router includes health endpoints
- **WHEN** `api_router` is configured
- **THEN** it SHALL include `health.router` with prefix `/health` and tags `["health"]`.

#### Scenario: Router includes dashboard endpoints
- **WHEN** `api_router` is configured
- **THEN** it SHALL include `dashboard.router` with prefix `/dashboard` and tags `["dashboard"]`.

#### Scenario: Router includes users endpoints
- **WHEN** `api_router` is configured
- **THEN** it SHALL include `users.router` with prefix `/users` and tags `["users"]`.

### Requirement: Health Endpoints
The system SHALL provide health check endpoints at both root and v1 paths for backward compatibility.

#### Scenario: Root health endpoint
- **WHEN** client requests `GET /health`
- **THEN** response SHALL be `{"status": "ok"}` with status 200.

#### Scenario: v1 health endpoint
- **WHEN** client requests `GET /api/v1/health`
- **THEN** response SHALL be `{"status": "ok"}` with status 200.

### Requirement: Dashboard Statistics Endpoint
The system SHALL provide a dashboard statistics endpoint.

#### Scenario: GET /api/v1/dashboard/stats
- **WHEN** client requests `GET /api/v1/dashboard/stats`
- **THEN** response SHALL be JSON with:
  - `total_users`: integer
  - `active_sessions`: integer
  - `api_calls_24h`: integer
- **AND** status code SHALL be 200.

### Requirement: Users List Endpoint
The system SHALL provide a users list endpoint.

#### Scenario: GET /api/v1/users
- **WHEN** client requests `GET /api/v1/users`
- **THEN** response SHALL be JSON array of user objects:
  - Each user: `{id: number, name: string, email: string, status: string}`
- **AND** status code SHALL be 200.

### Requirement: Health endpoint tests
The system SHALL include tests for both health endpoints.

#### Scenario: Root health test passes
- **WHEN** `test_root_health` is run
- **THEN** it SHALL verify `GET /health` returns 200 and `{"status": "ok"}`.

#### Scenario: v1 health test passes
- **WHEN** `test_v1_health` is run
- **THEN** it SHALL verify `GET /api/v1/health` returns 200 and `{"status": "ok"}`.

### Requirement: Dashboard stats endpoint test
The system SHALL include a test for the dashboard statistics endpoint.

#### Scenario: Dashboard stats test passes
- **WHEN** `test_dashboard_stats` is run
- **THEN** it SHALL verify `GET /api/v1/dashboard/stats` returns 200 with expected fields.

### Requirement: Users endpoint test
The system SHALL include a test for the users list endpoint.

#### Scenario: Users list test passes
- **WHEN** `test_users_list` is run
- **THEN** it SHALL verify `GET /api/v1/users` returns 200 with array of users.