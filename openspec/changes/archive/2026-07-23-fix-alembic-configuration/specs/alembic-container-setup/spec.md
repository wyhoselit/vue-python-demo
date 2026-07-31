## ADDED Requirements

### Requirement: Alembic configured for container environment
The system SHALL ensure Alembic `alembic.ini` and `env.py` are configured to operate correctly within a Docker/Podman container.

#### Scenario: `alembic.ini` uses dynamic URL
- **WHEN** Alembic is executed within the container
- **THEN** `alembic.ini` SHALL not contain a hardcoded `sqlalchemy.url` but rely on `env.py` to retrieve it.

#### Scenario: `env.py` imports application settings
- **WHEN** `alembic/env.py` is executed
- **THEN** it SHALL successfully import `settings` from `app.core.config` and `Base` from `app.core.database`.

#### Scenario: `env.py` uses `settings.DATABASE_URL`
- **WHEN** `env.py` configures the database connection
- **THEN** it SHALL use `settings.DATABASE_URL` as the connection string.

### Requirement: Dockerfile includes Alembic files
The `backend/Dockerfile` SHALL copy the `alembic/` directory and `alembic.ini` into the container image.

#### Scenario: Alembic files present in container
- **WHEN** `backend` container is built
- **THEN** `/app/alembic/` directory and `/app/alembic.ini` SHALL exist.

## MODIFIED Requirements

### Requirement: Alembic can upgrade and downgrade
The system SHALL support both upgrade and downgrade operations.

#### Scenario: Upgrade database
- **WHEN** running `alembic upgrade head` inside the container
- **THEN** system SHALL apply all pending migrations successfully.

#### Scenario: Downgrade database
- **WHEN** running `alembic downgrade -1` inside the container
- **THEN** system SHALL revert the last migration successfully.
