# Proposal: Fix Auto Migration on Startup

## Why
- `inspect(engine).get_table_names()` returns `[]` — tables not created on container startup
- Registration fails with `no such table: users`
- Currently requires manual `docker exec` + `alembic upgrade head`

## What
- Verify User model and Alembic detection
- Generate/create correct migration for `users` table
- Add automatic migration execution on container startup (before uvicorn)

## Scope
- `backend/app/models/user.py`
- `backend/alembic/env.py`
- `backend/alembic/versions/` (new migration)
- `backend/Dockerfile` or entrypoint script
- `backend/entrypoint.sh` (new)
- `README.md`