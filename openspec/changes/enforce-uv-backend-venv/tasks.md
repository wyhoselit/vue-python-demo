## 1. Environment Setup

- [x] 1.1 Install `uv` globally or add bootstrap script
- [x] 1.2 Create `backend/pyproject.toml` from existing `requirements.txt` if needed
- [x] 1.3 Add `.venv` to `.gitignore`
- [x] 1.4 Create `backend/.venv` using `uv venv .venv`

## 2. Dependency Management Migration

- [x] 2.1 Run `uv sync` to install dependencies from `pyproject.toml`
- [x] 2.2 Verify all existing packages work with `uv`
- [x] 2.3 Remove `backend/requirements.txt` (optional, if fully migrated to `pyproject.toml`)

## 3. Development Commands Update

- [x] 3.1 Update `docker-entrypoint.sh` to use `uv run` for backend commands
- [x] 3.2 Create `Makefile` or wrapper scripts:
  - `make install` → `uv sync`
  - `make test` → `uv run pytest`
  - `make run` → `uv run uvicorn app.main:app --reload`
  - `make migrate` → `uv run alembic upgrade head`
  - `make makemigrations` → `uv run alembic revision --autogenerate`
- [x] 3.3 Update `pytest.ini` if needed for `uv run` compatibility

## 4. Documentation

- [x] 4.1 Update `README.md` with `uv`-based workflow
- [x] 4.2 Update `setup.md` with `uv` installation and usage instructions
- [x] 4.3 Add environment verification section (e.g., `uv run python --version`)

## 5. CI/CD Pipeline

- [x] 5.1 Update GitHub Actions workflow to install `uv`
- [x] 5.2 Update CI steps to use `uv sync` and `uv run pytest`
- [x] 5.3 Verify CI passes with new environment

## 6. Verification

- [x] 6.1 Test fresh clone: `uv venv .venv && uv sync && uv run pytest`
- [x] 6.2 Test development server: `uv run uvicorn app.main:app --reload`
- [x] 6.3 Test migrations: `uv run alembic upgrade head`
- [x] 6.4 Confirm no system Python dependencies are required