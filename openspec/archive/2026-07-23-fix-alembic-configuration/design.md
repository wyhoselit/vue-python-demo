## Context

The previous change (`enhance-fastapi-backend`) initialized Alembic but did not fully configure it for consistent container-based execution. The `alembic.ini` file's `sqlalchemy.url` is not dynamically loaded from settings, and `env.py` needs adjustment to ensure `app.core.config` and `app.core.database` are correctly imported within the container's Python path. A robust solution requires integrating Alembic initialization and migration steps directly into the Docker build process or providing a clear entrypoint for it.

## Goals / Non-Goals

**Goals:**
- Alembic `upgrade head` command runs successfully within the `backend` container.
- `alembic.ini` correctly points to the database URL defined in `app.core.config.settings`.
- `backend/alembic/env.py` reliably imports application settings and database `Base` metadata.
- `backend/Dockerfile` ensures all necessary Alembic files are present and accessible.
- Provide a clear mechanism (e.g., entrypoint script) to run migrations during development or deployment.
- Update `README.md` with accurate Alembic usage instructions.

**Non-Goals:**
- Implement new database models or migrations. This change focuses purely on the configuration.
- Integrate Alembic into FastAPI lifespan events for automatic migrations (this is a separate decision with different trade-offs).
- Support multiple database configurations within Alembic beyond `DATABASE_URL`.

## Decisions

### 1. Centralized `sqlalchemy.url` in `alembic.ini`
**Choice:** Set `sqlalchemy.url` in `alembic.ini` to a placeholder or rely fully on `env.py`. `env.py` will pull from `app.core.config`.
**Rationale:** `env.py` is the most flexible place to set the database URL dynamically, ensuring it uses the same `DATABASE_URL` as the FastAPI application. Keeping `alembic.ini` simple prevents duplication.

### 2. Python Path in `env.py`
**Choice:** Add `sys.path.insert` in `alembic/env.py` to ensure `app` module is discoverable.
**Rationale:** Docker containers might not automatically have `/app` (or where the `app` package resides) in Python's `sys.path`, leading to import errors for `app.core.config` and `app.core.database`. Explicitly adding it ensures imports work consistently.

### 3. Dockerfile and Alembic Initialization
**Choice:** Copy `alembic/` directory into the Docker image. Rely on `alembic init` being run *once* outside the container (or in a separate ephemeral container) to generate the initial files, then commit them. The Dockerfile's role is then to *include* these pre-generated files.
**Rationale:** `alembic init` only needs to run once per project to scaffold the directory. Including these files directly in the image ensures they are always present.

### 4. Migration Execution Strategy
**Choice:** Document running `alembic upgrade head` manually via `podman exec` or via a custom entrypoint script for development, but not automatically in the main CMD.
**Rationale:** Automatic migrations on container startup can be risky in production environments (e.g., if a migration fails). Manual execution or a dedicated migration job provides more control. For development, a simple entrypoint script can automate this.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| `env.py` imports fail due to Python path issues | Explicitly add `sys.path.insert` in `env.py` to ensure `app` is discoverable. |
| Alembic configuration out of sync with app config | Ensure `env.py` sources `DATABASE_URL` directly from `app.core.config.settings`. |
| Unintended automatic migrations in production | Avoid automatic `alembic upgrade head` in main Docker CMD. Document manual execution or dedicated migration container. |
| Local alembic setup differs from container | Document that `alembic init` should be run once, then committed. Dockerfile copies these static files. |

## Open Questions

- Should `alembic.ini`'s `sqlalchemy.url` be completely removed or set to a dummy value, relying entirely on `env.py`? (Decided: rely on `env.py` to overwrite it with `config.set_main_option`)
- Should a specific `.env.alembic` file be used for Alembic config, or the main `.env`? (Decided: use main `.env` through `app.core.config` for consistency)
