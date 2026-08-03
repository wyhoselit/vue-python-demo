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

The backend is structured as a modular application under `backend/app/modules/`:

```
backend/
├── app/
│   ├── main.py           # Main FastAPI application entry point
│   ├── api/              # API routing and versioning
│   │   ├── v1/           # API v1 endpoints (legacy)
│   │   ├── v2/           # API v2 endpoints (current)
│   │   └── version_router.py
│   │   └── versioning.py
│   ├── modules/          # Feature modules (see below)
│   │   ├── admin/        # Admin API (logs, tracing, status)
│   │   ├── core/         # Core functionality (config, database, security)
│   │   ├── dashboard/    # Dashboard API
│   │   ├── system/       # System health and configuration
│   │   └── user/         # User management and authentication
│   └── core/             # Legacy core module references
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

### Modules Structure

- **admin**: Admin-only endpoints for logs, tracing, and system status
- **core**: Shared configuration, database, and security utilities
- **dashboard**: Dashboard API for statistics and data
- **system**: System settings service and configuration management
- **user**: User authentication and profile management

### System Module

The system module centralizes application-wide configuration and settings storage. It provides a consistent service-based interface (`SettingService`) for managing settings, replacing fragmented configuration tables (like tracing configuration) with a unified `SystemSetting` model.

- **`SystemSetting` model**: Defines storage for system-wide configuration keys and values (`backend/app/modules/system/models/system_setting.py`).
- **`SettingService`**: Implements CRUD and management logic for system settings (`backend/app/modules/system/services/setting_service.py`).


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

## API Versioning

The backend supports multi-version API routing via `backend/app/api/version_router.py`.

- **v1**: Deprecated/legacy endpoints.
- **v2**: Current active API.

All versioning logic is centralized in `backend/app/api/versioning.py`.

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
