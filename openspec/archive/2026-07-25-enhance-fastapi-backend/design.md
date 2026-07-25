## Context

Current backend is a minimal FastAPI app with single `/health` endpoint. No configuration management, no database layer, no structured API versioning. Runs in Podman container with hot-reload via volume mount. Frontend on port 5173 needs CORS access.

## Goals / Non-Goals

**Goals:**
- Enterprise-grade project structure with separation of concerns
- Centralized configuration via Pydantic Settings (env vars)
- PostgreSQL-ready database layer with SQLAlchemy
- API versioning foundation (v1 router structure)
- CORS middleware for frontend integration
- Global exception handling
- Alembic migration setup
- Maintain Podman/docker-compose compatibility

**Non-Goals:**
- Authentication/JWT implementation (security.py stub only)
- Actual database models or migrations beyond initialization
- API endpoints beyond moving existing health check
- Production deployment configuration

## Decisions

### 1. Configuration: Pydantic Settings
**Choice:** Use `pydantic-settings` with BaseSettings
**Rationale:** Type-safe, automatic env var loading, validation built-in. Standard in FastAPI ecosystem.
**Alternatives:** python-dotenv (manual parsing), dynaconf (overkill for this scope)

### 2. Database: SQLAlchemy 2.0 async-ready pattern
**Choice:** SQLAlchemy with async engine, sessionmaker
**Rationale:** Future-proof for async endpoints. PostgreSQL support via asyncpg/psycopg.
**Alternatives:** Tortoise ORM (less mature), raw asyncpg (no ORM benefits)
**Note:** Use sync driver psycopg2-binary initially for simplicity; async migration is non-breaking later.

### 3. API Versioning: Router-based
**Choice:** `app/api/v1/` with APIRouter, mounted at `/api/v1` in main.py
**Rationale:** Clean URL structure, easy to add v2 later, follows FastAPI best practices.
**Alternatives:** Subdomain versioning (infrastructure complexity), header versioning (harder to test)

### 4. CORS: Allow localhost:5173
**Choice:** Middleware with explicit origin list
**Rationale:** Explicit allowlist is more secure than wildcard. Easy to extend for staging/prod.
**Alternatives:** `allow_origins=["*"]` (insecure for production)

### 5. Exception Handling: Global handlers
**Choice:** FastAPI exception_handlers in main.py
**Rationale:** Centralized error response format, catches unhandled exceptions.
**Alternatives:** Per-router error handling (scattered, inconsistent)

### 6. Alembic: Single-database setup
**Choice:** `alembic init alembic` with SQLAlchemy URL from config
**Rationale:** Industry standard for SQLAlchemy migrations. Config-driven.
**Alternatives:** Manual migration scripts (error-prone), no migrations (unacceptable for production)

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Config changes require container restart | Document env var updates in README; Podman Compose supports .env reload |
| Async DB driver adds complexity | Start with sync psycopg2-binary; document async upgrade path |
| Alembic config hardcoded to PostgreSQL | Use env var for DATABASE_URL; support SQLite for local dev |
| CORS origin hardcoded to localhost | Use config CORS_ORIGINS list; default to localhost:5173 |

## Migration Plan

1. Create new core/api modules (non-breaking, additive)
2. Refactor main.py to use new modules
3. Initialize Alembic (no models yet, empty migration)
4. Update requirements.txt
5. Rebuild container images
6. Verify health endpoint still works at `/health` and `/api/v1/health`
7. Update README with architecture diagram

**Rollback:** Revert main.py changes, remove new directories, restore requirements.txt. Container stateless, no data migration.
