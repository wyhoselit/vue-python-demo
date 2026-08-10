#!/bin/bash
set -e

echo "Running Alembic migrations..."
uv run alembic upgrade head

echo "Running initialization..."
uv run python init_db.py

echo "Starting FastAPI application..."
exec uv run "$@"