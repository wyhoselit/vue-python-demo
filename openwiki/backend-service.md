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
│   └── main.py       # Main FastAPI application entry point
├── requirements.txt  # Python dependencies
└── Dockerfile        # Docker build instructions
```

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

## Source References

-   Main application file: `backend/app/main.py`
-   Dependencies: `backend/requirements.txt`
-   Docker build file: `backend/Dockerfile`
