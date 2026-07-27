## 1. Model & Migration

- [x] 1.1 Verify `backend/app/models/user.py` is correct
- [x] 1.2 Update `backend/alembic/env.py` to import User model for target_metadata
- [x] 1.3 Generate `create_users_table` migration if missing
- [x] 1.4 Apply migration locally to verify

## 2. Auto Migration on Startup

- [x] 2.1 Create `backend/entrypoint.sh` with `alembic upgrade head` + uvicorn
- [x] 2.2 Update `backend/Dockerfile` to copy and use entrypoint
- [x] 2.3 Make entrypoint executable

## 3. Testing & Verification

- [x] 3.1 Rebuild and restart containers (`podman-compose down && podman-compose up -d --build`)
- [x] 3.2 Verify `users` table exists after startup
- [x] 3.3 Test registration endpoint works

## 4. Documentation

- [x] 4.1 Update `README.md` with auto-migration explanation