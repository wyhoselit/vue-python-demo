# Docker Orchestration Specification

## Purpose
Provides Docker Compose configuration for running both backend and frontend services together.

## Requirements

### Requirement: Docker Compose configuration
The project SHALL provide a `docker-compose.yml` at the repository root that defines services for both backend and frontend.

#### Scenario: Docker Compose file exists
- **WHEN** the repository is cloned
- **THEN** `docker-compose.yml` SHALL exist at the root with `backend` and `frontend` services defined

### Requirement: Backend Dockerfile
The backend SHALL include a `Dockerfile` that builds a runnable Python image.

#### Scenario: Backend container starts
- **WHEN** `docker compose up backend` is run
- **THEN** the backend service SHALL start and respond to `GET /health`

### Requirement: Frontend Dockerfile
The frontend SHALL include a `Dockerfile` that builds and serves the Vue application.

#### Scenario: Frontend container starts
- **WHEN** `docker compose up frontend` is run
- **THEN** the frontend service SHALL start and serve the application on its configured port

### Requirement: Environment configuration
The project SHALL provide a `.env.example` file documenting required environment variables.

#### Scenario: Env example file exists
- **WHEN** the repository is cloned
- **THEN** `.env.example` SHALL exist at the root with documented variable placeholders