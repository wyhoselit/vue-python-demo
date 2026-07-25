## Why

The backend currently lacks a standardized, reliable, and performant Python environment management. Using the system Python environment and `pip` creates reproducibility issues and dependency conflicts. Enforcing a project-local `.venv` managed exclusively by `uv` provides industry-leading dependency resolution speed, project isolation, and robust environment reproduction.

## What Changes

- Enforce `.venv` in the backend directory as the sole Python environment
- Replace `pip` with `uv` for all dependency management (`uv sync`, `uv add`, `uv run`)
- Update `README.md` and `setup.md` to document the new `uv` workflow
- Update `docker-entrypoint.sh` and CI/CD pipelines to use `uv`
- Add `.venv` to `.gitignore`
- Remove reliance on global `pip` and system Python packages

## Capabilities

### New Capabilities

- `uv-backend-venv-management`: Automated virtual environment setup and dependency management using `uv`

### Modified Capabilities

- `backend-testing`: Tests must run via `uv run pytest`
- `backend-development`: Development commands must run via `uv run`
- `backend-dependency-management`: All dependency changes must go through `uv add`/`uv sync`

## Impact

- `backend/requirements.txt`: Migration to `pyproject.toml` (if not already present) or managed by `uv`
- `backend/Makefile` / shell scripts: Commands updated to use `uv`
- `docker-entrypoint.sh`: Updated for `uv` environment
- `README.md` / `setup.md`: Documentation updated
- CI/CD pipelines: Updated to use `uv`
