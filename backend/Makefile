.PHONY: install test run migrate makemigrations shell lint format docs docs-serve docs-openapi

install:
	uv sync

test:
	uv run pytest

run:
	uv run uvicorn app.main:app --reload

migrate:
	uv run alembic upgrade head

makemigrations:
	uv run alembic revision --autogenerate -m "$(message)"

shell:
	uv run python

lint:
	uv run ruff check .

format:
	uv run ruff format .

docs:
	uv run mkdocs build --strict

docs-serve:
	uv run mkdocs serve

docs-openapi:
	uv run python scripts/update_openapi.py