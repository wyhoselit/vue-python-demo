#!/bin/bash
set -e

if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running Alembic migrations..."
    uv run alembic upgrade head
    echo "Migrations complete."
fi

exec uv run "$@"
