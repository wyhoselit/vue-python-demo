# Full-Stack Demo (Vuetify + FastAPI)

A monorepo demo application with a Vue 3 + Vuetify frontend and FastAPI backend.

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)

## Project Structure

```
.
├── backend/          # FastAPI backend
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # Vue 3 + Vuetify frontend
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker/
├── docker-compose.yml
└── .env.example
```

## Local Development

### Backend

The FastAPI backend is structured for enterprise-grade scalability and maintainability.

**Architecture:**
- **Core Module (`app/core/`)**:
  - `config.py`: Centralized configuration using Pydantic Settings, loading environment variables from `.env`.
  - `database.py`: SQLAlchemy engine and session management for PostgreSQL/SQLite, with a FastAPI dependency for database sessions.
  - `security.py`: Stub for JWT token creation and verification (future use).
- **API Versioning (`app/api/v1/`)**:
  - Uses `APIRouter` for versioned endpoints, mounted at `/api/v1`.
  - Health check is available at `/api/v1/health` and legacy `/health`.
- **Middleware**: Configured with CORS to allow frontend communication (e.g., from `http://localhost:5173`).
- **Error Handling**: Global exception handlers for `HTTPException` and unhandled exceptions provide consistent JSON responses.
- **Alembic**: Database migration tool configured to manage schema changes.

**Setup & Run:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
**Alembic Migrations in Docker/Podman:**

For Alembic to function correctly within the containerized environment:

1.  **Generate initial Alembic files**: If not already present, run `podman run --rm -v $(pwd)/backend:/app --entrypoint "alembic" localhost/demo_backend:latest init alembic` from the project root. This creates the `backend/alembic` directory and `backend/alembic.ini`. **Commit these generated files.**
2.  **Run migrations**:
    -   To apply pending migrations: `podman exec -it demo_backend_1 alembic upgrade head`
    -   To generate a new migration script (after model changes): `podman exec -it demo_backend_1 alembic revision --autogenerate -m "Description of changes"`
    -   To rollback last migration: `podman exec -it demo_backend_1 alembic downgrade -1`
3.  **Optional: Auto-run migrations on startup (for development)**:
    Set the environment variable `RUN_MIGRATIONS=true` when starting the backend service.
    Example: `RUN_MIGRATIONS=true podman-compose up -d --build backend`
    This uses the `docker-entrypoint.sh` script to run `alembic upgrade head` before starting the FastAPI app.

Backend runs at http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

### Running Tests

#### Backend Tests

```bash
cd backend
pip install pytest httpx pytest-asyncio
pytest
```

#### Frontend Tests

```bash
cd frontend
npm run test
```

#### Run All Tests

```bash
# Run backend tests
cd backend && pytest

# Run frontend tests
cd frontend && npm run test
```

## Docker

```bash
cp .env.example .env
docker compose up
```

## Podman

```bash
cp .env.example .env
podman compose up
```


- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health check: http://localhost:8000/health
