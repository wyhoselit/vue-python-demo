## 1. Alembic Configuration
- [x] 1.1 Modify `backend/alembic.ini`: Set `sqlalchemy.url` to a dummy value or remove it entirely, relying on `env.py`.
- [x] 1.2 Modify `backend/alembic.ini`: Ensure `script_location` is set correctly relative to the `alembic.ini` file.

## 2. Alembic Environment Script (`env.py`)
- [x] 2.1 Modify `backend/alembic/env.py`: Add `sys.path.insert` to include the `app` directory for imports.
- [x] 2.2 Modify `backend/alembic/env.py`: Import `settings` from `app.core.config`.
- [x] 2.3 Modify `backend/alembic/env.py`: Import `Base` from `app.core.database` and set `target_metadata = Base.metadata`.
- [x] 2.4 Modify `backend/alembic/env.py`: Use `settings.DATABASE_URL` for `sqlalchemy.url` in `config.set_main_option`.
- [x] 2.5 Modify `backend/alembic/env.py`: Update `run_migrations_online` to use an async-compatible engine if `settings.DATABASE_URL` suggests it (e.g., `postgresql+asyncpg`). For now, keep it synchronous as the app uses a synchronous engine, and Alembic's `env.py` can be synchronous even with an async app.

## 3. Dockerfile Adjustments
- [x] 3.1 Modify `backend/Dockerfile`: Copy `alembic.ini` and the `alembic/` directory into the `/app` directory in the container.

## 4. Migration Execution (Optional Entrypoint)
- [x] 4.1 Create `backend/docker-entrypoint.sh`: A shell script to run `alembic upgrade head` conditionally, e.g., only if a specific environment variable is set.
- [x] 4.2 Modify `backend/Dockerfile`: Add `COPY docker-entrypoint.sh /usr/local/bin/` and `RUN chmod +x /usr/local/bin/docker-entrypoint.sh`.
- [x] 4.3 Modify `backend/Dockerfile`: Change `CMD` to `CMD ["docker-entrypoint.sh", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]` (or similar, ensuring it runs our entrypoint script).

## 5. Documentation Update
- [x] 5.1 Update `README.md` (Backend section): Add clear instructions on how to use Alembic for migrations, including `podman exec` commands and notes on Dockerfile/entrypoint integration.

## 6. Verification
- [x] 6.1 Rebuild backend container: `podman-compose build backend`
- [x] 6.2 Run `podman-compose up -d` to start services.
- [x] 6.3 Execute `alembic upgrade head` inside the container: `podman exec -it demo_backend_1 alembic upgrade head` and verify successful execution.
- [x] 6.4 (If implemented) Test entrypoint migration: `podman-compose down && PODMAN_RUN_MIGRATIONS=true podman-compose up -d --build` (or similar env var).