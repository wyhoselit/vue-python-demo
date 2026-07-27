## Context
- SQLite used in dev (`sqlite:///./app.db`)
- Alembic configured but no auto-run on startup
- User model exists but no migration created/applied

## Goals / Non-Goals
**Goals:**
- User model correctly detected by Alembic
- Migration creates `users` table with `id`, `email`, `hashed_password`
- `alembic upgrade head` runs automatically on container start
- Clear logs if migration fails; app does not start

**Non-Goals:**
- Production PostgreSQL setup (separate concern)
- Data seeding

## Decisions
1. **Entrypoint Script**: New `entrypoint.sh` runs migration then starts uvicorn
2. **Dockerfile**: Copy entrypoint, set as ENTRYPOINT
3. **Alembic env.py**: Ensure `target_metadata` imports all models (`from app.models.user import User`)
4. **Migration**: Create `create_users_table` if not exists

## Risks / Trade-offs
- Entrypoint adds ~2-3s startup delay (acceptable for dev)
- SQLite file persisted in volume; migration idempotent