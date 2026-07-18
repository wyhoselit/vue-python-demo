## Context

This is a greenfield project. We need a clean monorepo structure to support a Vuetify + FastAPI full-stack demo application. No existing code or architecture constraints exist.

## Goals / Non-Goals

**Goals:**
- Establish a clear separation between frontend and backend code
- Enable local development with hot-reload for both services
- Provide Docker Compose for one-command startup
- Keep the skeleton minimal and extensible

**Non-Goals:**
- Authentication or authorization
- Database setup or ORM configuration
- CI/CD pipelines
- Production-grade security hardening

## Decisions

### 1. Monorepo structure with separate directories

**Choice**: Root-level `backend/` and `frontend/` directories.

**Rationale**: Simple, standard pattern for full-stack projects. Each service can have its own dependency management while sharing the repo root for Docker Compose and documentation.

**Alternatives considered**:
- Separate repos: Adds complexity for a demo project
- Nested structure (e.g., `src/backend/`): Unnecessarily deep

### 2. FastAPI with minimal dependencies

**Choice**: Use `fastapi`, `uvicorn[standard]`, and `pydantic-settings`.

**Rationale**: FastAPI provides async support and automatic OpenAPI docs. Uvicorn is the standard ASGI server. Pydantic-settings enables `.env` file loading for configuration.

**Alternatives considered**:
- Flask: Less modern, no async by default
- Django: Too heavy for a minimal skeleton

### 3. Vue 3 + TypeScript + Vite + Vuetify 3

**Choice**: Use the official Vue TypeScript template with Vuetify 3 plugin.

**Rationale**: TypeScript catches errors early. Vite provides fast HMR. Vuetify 3 offers Material Design components with Vue 3 Composition API support.

**Alternatives considered**:
- plain JavaScript: Loses type safety
- Nuxt: Overkill for a demo SPA

### 4. Docker Compose for orchestration

**Choice**: Single `docker-compose.yml` with `backend` and `frontend` services.

**Rationale**: Simple one-command startup. Each service gets its own Dockerfile for production builds. Development mode mounts source code as volumes.

**Alternatives considered**:
- Docker only (no Compose): Requires manual multi-container management
- Podman: Less ecosystem support for demos

## Risks / Trade-offs

- **Risk**: Vuetify 3 may have breaking changes in future minor versions. **Mitigation**: Pin Vuetify version in package.json.
- **Risk**: No database means backend health endpoint is trivial. **Mitigation**: Acceptable for skeleton; database will be added in a later change.
- **Trade-off**: Using separate `requirements.txt` (backend) and `package.json` (frontend) instead of a unified build tool. **Acceptable**: Keeps each service independently understandable.
