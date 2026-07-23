## Why

Current FastAPI backend lacks enterprise-grade structure: no centralized configuration, no database layer, no API versioning, no CORS/security middleware. Podman deployment works but codebase cannot scale for production features.

## What Changes

- Add `app/core/config.py` with Pydantic Settings for environment variables (DATABASE_URL, SECRET_KEY, DEBUG, etc.)
- Add `app/core/database.py` with SQLAlchemy engine and session management (PostgreSQL-ready)
- Add `app/core/security.py` with JWT configuration stub
- Create `app/api/v1/` router structure with versioned endpoints
- Move health endpoint to `app/api/v1/endpoints/health.py`
- Add CORS middleware allowing `http://localhost:5173`
- Add global exception handlers
- Refactor `main.py` to cleanly integrate all modules
- Update `requirements.txt` with sqlalchemy, alembic, psycopg2-binary, python-jose[cryptography], passlib[bcrypt]
- Initialize Alembic for database migrations
- Update README.md with backend architecture documentation

## Capabilities

### New Capabilities
- `core-config`: Centralized configuration management using Pydantic Settings
- `database-layer`: SQLAlchemy database engine and session management
- `api-versioning`: Versioned API router structure (v1)
- `cors-middleware`: CORS configuration for frontend integration
- `error-handling`: Global exception handlers
- `alembic-migrations`: Database migration setup

### Modified Capabilities
- None (no existing specs)

## Impact

- New files: `app/core/`, `app/api/v1/`, `alembic/`
- Modified: `app/main.py`, `requirements.txt`, `README.md`
- Dependencies: sqlalchemy, alembic, psycopg2-binary, python-jose, passlib
- Podman/docker-compose compatibility maintained
