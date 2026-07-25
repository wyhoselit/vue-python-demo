## Context

The backend currently relies on the system Python environment and `pip`, leading to inconsistencies and poor reproducibility.

## Goals / Non-Goals

**Goals:**
- Use project-local `.venv` as the sole Python environment
- Use `uv` for all dependency management (`sync`, `add`, `run`)
- Guarantee zero reliance on global `pip` or system Python

**Non-Goals:**
- Removing the Docker isolation (Docker is complementary)

## Decisions

1. **Environment Manager**: Adopt `uv` for its performance and robustness.
2. **Environment Activation**: Commands will be run via `uv run` instead of requiring manual environment activation.
3. **Dependency Source of Truth**: Use `pyproject.toml` managed by `uv` for dependencies.

## Risks / Trade-offs

- [Developer learning curve] → Provide a `Makefile` with simple commands (`make install`, `make test`).
- [CI/CD migration] → Requires updated environment setup in pipelines.

## Migration Plan

1. Install `uv` globally or via a bootstrap script.
2. Replace `pip install -r requirements.txt` with `uv sync`.
3. Update `docker-entrypoint.sh` to use `uv run`.
4. Update CI/CD steps to use `uv`.
5. Remove system-level dependencies.

## Verification Criteria

All verification tasks in section 6 must pass:
- **6.1 Fresh Clone Test**: Repository can be cloned and run without pre-existing Python environment.
- **6.2 Development Server Test**: Development server starts and responds correctly.
- **6.3 Migration Test**: Database migrations apply successfully.
- **6.4 Isolation Test**: No system Python or global pip dependencies are required.
