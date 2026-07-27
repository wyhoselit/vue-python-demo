## ADDED Requirements

### Requirement: Auto Migration on Container Startup
The system SHALL automatically run Alembic migrations when the backend container starts, before the FastAPI application begins accepting requests.

#### Scenario: Successful migration on clean database
- **WHEN** a fresh backend container starts with an empty SQLite database
- **THEN** `alembic upgrade head` executes and creates all tables including `users`
- **AND** FastAPI application starts only after migration completes successfully

#### Scenario: Successful migration on existing database
- **WHEN** a backend container starts with an existing database at an older revision
- **THEN** `alembic upgrade head` applies pending migrations
- **AND** FastAPI application starts only after all migrations complete

#### Scenario: Migration failure blocks startup
- **WHEN** `alembic upgrade head` fails (e.g., constraint violation, syntax error)
- **THEN** container exits with non-zero code
- **AND** error message is logged clearly
- **AND** FastAPI application does NOT start

### Requirement: User Table Schema
The system SHALL create a `users` table with the following schema on first migration.

#### Scenario: users table structure
- **WHEN** migration `create_users_table` is applied
- **THEN** table `users` exists with columns:
  - `id` INTEGER PRIMARY KEY AUTOINCREMENT
  - `email` VARCHAR UNIQUE NOT NULL
  - `hashed_password` VARCHAR NOT NULL

### Requirement: User Model Detection by Alembic
Alembic SHALL correctly detect the `User` model from `app.models.user` for autogenerate.

#### Scenario: autogenerate detects User model
- **WHEN** running `alembic revision --autogenerate -m "create_users_table"`
- **THEN** generated migration includes `CREATE TABLE users` with correct columns