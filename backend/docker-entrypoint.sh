#!/bin/bash
set -e

if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running Alembic migrations..."
    alembic upgrade head
    echo "Migrations complete."
fi

exec "$@"