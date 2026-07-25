## ADDED Requirements

### Requirement: Project virtual environment creation via uv
The system SHALL provide a mechanism to create a `.venv` virtual environment in the backend directory using `uv`.

#### Scenario: Create virtual environment with uv
- **WHEN** user runs `uv venv .venv` in the backend directory
- **THEN** a `.venv` directory is created in the backend directory
- **AND** the directory contains a Python interpreter and `uv` managed environment

### Requirement: Dependency synchronization via uv
The system SHALL install and synchronize all dependencies from `pyproject.toml` into the `.venv` virtual environment using `uv sync`.

#### Scenario: Sync dependencies
- **WHEN** user runs `uv sync` in the backend directory
- **THEN** all packages in `pyproject.toml` are installed/updated in `.venv`
- **AND** the lock file is updated to reflect exact versions

### Requirement: Dependency addition via uv
The system SHALL add new dependencies to the project using `uv add`.

#### Scenario: Add new dependency
- **WHEN** user runs `uv add <package>` in the backend directory
- **THEN** `<package>` is added to `pyproject.toml`
- **AND** `<package>` is installed in `.venv`
- **AND** lock file is updated

### Requirement: Command execution via uv run
The system SHALL execute all backend commands (pytest, uvicorn, alembic, etc.) via `uv run` to ensure the `.venv` environment is used.

#### Scenario: Run tests with uv run
- **WHEN** user runs `uv run pytest`
- **THEN** tests execute using `.venv` Python interpreter
- **AND** test results reflect `.venv` installed packages

#### Scenario: Run development server with uv run
- **WHEN** user runs `uv run uvicorn app.main:app`
- **THEN** server starts using `.venv` Python and dependencies

#### Scenario: Run migrations with uv run
- **WHEN** user runs `uv run alembic upgrade head`
- **THEN** migrations run using `.venv` environment

### Requirement: Environment isolation enforcement
The system SHALL NOT rely on system Python, global pip, or external virtual environments for backend operations.

#### Scenario: No system Python usage
- **WHEN** any backend command is executed
- **THEN** it MUST be invoked via `uv run` or within an activated `.venv`

### Requirement: CI/CD integration with uv
The system SHALL configure CI/CD pipelines to use `uv` for environment setup and command execution.

#### Scenario: GitHub Actions uses uv
- **WHEN** GitHub Actions workflow runs on backend code
- **THEN** workflow installs `uv`
- **AND** runs `uv sync` to set up environment
- **AND** executes tests via `uv run pytest`