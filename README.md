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
# Initialize Alembic (if not already done)
alembic init alembic
# Update alembic/env.py to use app.core.config.settings.DATABASE_URL
# Generate initial migration
alembic revision --autogenerate -m "Initial migration"
# Run migrations
alembic upgrade head
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

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
