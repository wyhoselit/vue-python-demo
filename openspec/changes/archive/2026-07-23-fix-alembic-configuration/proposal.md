## Why

Alembic configuration was initialized during previous change but has issues: `alembic.ini` has hardcoded URL, `env.py` may not properly import settings in container context, and migrations cannot run reliably after Docker rebuild. Need permanent fix so `alembic upgrade head` works consistently in containers.

## What Changes

- Fix `backend/alembic.ini` to use environment variable or remove hardcoded URL
- Fix `backend/alembic/env.py` to properly import settings and use `DATABASE_URL`
- Update `backend/Dockerfile` to ensure alembic files are copied correctly
- Add entrypoint script option to run migrations on container start (dev mode)
- Update `README.md` with migration commands and troubleshooting

## Capabilities

### New Capabilities
- `alembic-container-setup`: Alembic configuration that works reliably in Docker/Podman containers with environment-based database URL

### Modified Capabilities
- `alembic-migrations`: Update requirements to support container-based migration execution

## Impact

- Modified: `backend/alembic.ini`, `backend/alembic/env.py`, `backend/Dockerfile`, `README.md`
- New: `backend/docker-entrypoint.sh` (optional migration runner)
- All existing migrations remain compatible
- Container rebuild will have working alembic configuration
