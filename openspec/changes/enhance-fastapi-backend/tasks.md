## 1. Core Configuration Module

- [ ] 1.1 Create `backend/app/core/__init__.py`
- [ ] 1.2 Create `backend/app/core/config.py` with Pydantic Settings class
- [ ] 1.3 Add `pydantic-settings` to `backend/requirements.txt`

## 2. Database Layer

- [ ] 2.1 Create `backend/app/core/database.py` with SQLAlchemy engine setup
- [ ] 2.2 Add database dependencies: `sqlalchemy`, `psycopg2-binary` to `backend/requirements.txt`
- [ ] 2.3 Create `backend/app/core/security.py` with JWT stub

## 3. API Versioning Structure

- [ ] 3.1 Create `backend/app/api/__init__.py`
- [ ] 3.2 Create `backend/app/api/v1/__init__.py` with APIRouter
- [ ] 3.3 Create `backend/app/api/v1/endpoints/__init__.py`
- [ ] 3.4 Create `backend/app/api/v1/endpoints/health.py` with health endpoint

## 4. Middleware and Error Handling

- [ ] 4.1 Add CORS middleware configuration to main.py
- [ ] 4.2 Add global exception handlers to main.py
- [ ] 4.3 Refactor `backend/app/main.py` to integrate all modules

## 5. Alembic Migrations

- [ ] 5.1 Initialize Alembic in backend directory
- [ ] 5.2 Configure `alembic/env.py` to use database URL from settings
- [ ] 5.3 Create initial empty migration

## 6. Documentation and Verification

- [ ] 6.1 Update `backend/requirements.txt` with all new dependencies
- [ ] 6.2 Update `README.md` with backend architecture documentation
- [ ] 6.3 Rebuild containers with `podman-compose up -d --build`
- [ ] 6.4 Verify `/health` endpoint returns `{"status": "ok"}`
- [ ] 6.5 Verify `/api/v1/health` endpoint returns `{"status": "ok"}`
- [ ] 6.6 Verify CORS headers present for localhost:5173
