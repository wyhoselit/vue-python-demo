## ADDED Requirements

### Requirement: API v1 router created
The system SHALL provide an APIRouter for version 1 endpoints.

#### Scenario: Router accessible
- **WHEN** code imports `api_router` from `app.api.v1`
- **THEN** system SHALL return the v1 APIRouter instance

### Requirement: Versioned endpoint structure
The system SHALL organize endpoints under `app/api/v1/endpoints/` directory.

#### Scenario: Endpoint module exists
- **WHEN** endpoint is defined in `app/api/v1/endpoints/health.py`
- **THEN** system SHALL make it importable from that path

### Requirement: Health endpoint available at v1 path
The system SHALL expose the health check endpoint at `/api/v1/health`.

#### Scenario: Health endpoint returns status
- **WHEN** client requests `GET /api/v1/health`
- **THEN** system SHALL return `{"status": "ok"}`

### Requirement: Backward compatibility for root health endpoint
The system SHALL continue to expose health check at `/health` for backward compatibility.

#### Scenario: Root health endpoint still works
- **WHEN** client requests `GET /health`
- **THEN** system SHALL return `{"status": "ok"}`

### Requirement: API prefix configurable
The system SHALL use API_V1_PREFIX configuration for the v1 router prefix.

#### Scenario: Custom prefix applied
- **WHEN** API_V1_PREFIX is set to `/api/v1`
- **THEN** system SHALL mount v1 router at `/api/v1`
