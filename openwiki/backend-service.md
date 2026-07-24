---
type: Service
title: Backend Service
description: FastAPI backend application with a health check endpoint.
tags: [fastapi, python, backend, microservice]
---

# Backend Service

The backend service is a FastAPI application providing a RESTful API.

## Technology Stack

- **Framework**: FastAPI
- **Language**: Python 3.10+
- **ASGI Server**: Uvicorn
- **Dependency Management**: `requirements.txt` (pip)
- **Configuration**: `pydantic-settings` for environment variable management

## Key Features

- **Health Check**: An essential `/health` endpoint for readiness and liveness probes.

## Architecture

The backend is structured as follows:

```
backend/
├── app/
│   ├── main.py           # Main FastAPI application entry point
│   ├── api/              # API routers and endpoints
│   │   ├── v1/
│   │   │   └── endpoints/ # Versioned API endpoints
│   │   └── router.py
│   └── core/             # Core configuration and database
│       ├── config.py     # Pydantic Settings configuration
│       ├── database.py   # SQLAlchemy engine and session
│       └── security.py
├── tests/                # Pytest test suite
│   ├── conftest.py       # Test fixtures
│   ├── test_api_*.py     # API endpoint tests
│   └── test_*.py         # Component tests
├── requirements.txt      # Python dependencies
├── pytest.ini            # Pytest configuration
├── Dockerfile            # Docker build instructions
├── docker-entrypoint.sh  # Container entrypoint with migration support
└── alembic/              # Database migrations
```

### Docker Entrypoint

The `docker-entrypoint.sh` script supports automatic Alembic migrations when `RUN_MIGRATIONS=true` is set in the environment.

## Getting Started (Local)

To run the backend service locally:

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Start the Uvicorn server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The backend will be accessible at `http://localhost:8000`.

## Endpoints

-   **`GET /health`**: Returns `{"status": "ok"}`.

## Testing

### Running Tests Locally

```bash
cd backend
pip install pytest httpx pytest-asyncio
pytest
```

### Test Coverage

- `tests/test_api_health.py` - Health endpoint tests
- `tests/test_config.py` - Configuration validation tests
- `tests/test_database.py` - Database connection and session tests
- `tests/test_api_cors.py` - CORS middleware tests
- `tests/test_api_errors.py` - Error handling tests

### Test Fixtures

`tests/conftest.py` provides:
- SQLite in-memory database fixture
- FastAPI TestClient fixture with dependency overrides
- Database session fixture

## Source References

-   Main application file: `backend/app/main.py`
-   Dependencies: `backend/requirements.txt`
-   Docker build file: `backend/Dockerfile`
