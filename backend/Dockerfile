FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Copy pyproject.toml and uv.lock
COPY pyproject.toml uv.lock ./

# Install dependencies with uv
RUN uv sync --frozen --no-install-project

COPY alembic/ ./alembic/
COPY alembic.ini .
COPY app/ ./app/
COPY tests/ ./tests/
COPY pytest.ini .

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]