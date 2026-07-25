## Context

The monorepo structure for the full-stack demo application is already established with `backend/` and `frontend/` directories. The frontend uses Vue 3 + TypeScript + Vite with Vuetify 3, and the backend uses FastAPI. The key integration point is `App.vue` which must correctly use `DefaultLayout` to render page content via `<router-view />`.

## Goals / Non-Goals

**Goals:**
- Verify `App.vue` correctly uses `DefaultLayout` with `<router-view />` for proper layout integration
- Ensure Docker Compose can start both services successfully
- Provide documentation (`.env.example`, `README.md`) with setup instructions

**Non-Goals:**
- Authentication or authorization
- Database setup or ORM configuration
- CI/CD pipelines
- Production-grade security hardening

## Decisions

### 1. App.vue Layout Integration

**Choice**: `<DefaultLayout><router-view /></DefaultLayout>` structure.

**Rationale**: The `DefaultLayout` component contains the Vuetify `v-app`, `v-app-bar`, and `v-main` elements. The `router-view` is nested inside `v-main` within `DefaultLayout.vue`. This keeps page content properly integrated with the application layout.

**Alternatives considered**:
- Direct Vuetify elements in App.vue: Would duplicate layout code and create maintenance burden
- No layout wrapper: Would lose consistent UI structure

### 2. Docker Compose for orchestration

**Choice**: Single `docker-compose.yml` with `backend` and `frontend` services.

**Rationale**: Simple one-command startup. Each service gets its own Dockerfile for production builds. Development mode mounts source code as volumes.

**Alternatives considered**:
- Docker only (no Compose): Requires manual multi-container management
- Podman: Less ecosystem support for demos

## Risks / Trade-offs

- **Risk**: Vuetify 3 may have breaking changes in future minor versions. **Mitigation**: Pin Vuetify version in package.json.
- **Risk**: No database means backend health endpoint is trivial. **Mitigation**: Acceptable for skeleton; database will be added in a later change.
- **Trade-off**: Using separate `requirements.txt` (backend) and `package.json` (frontend) instead of a unified build tool. **Acceptable**: Keeps each service independently understandable.
