# Backend Database Layer Specification

## Purpose
Defines the SQLAlchemy database configuration including engine, session management, and declarative base for ORM models.

## Requirements

### Requirement: SQLAlchemy engine initialization
The system SHALL create a SQLAlchemy engine using the `DATABASE_URL` from configuration.

#### Scenario: Engine created with PostgreSQL URL
- **WHEN** `DATABASE_URL` starts with `postgresql://`
- **THEN** engine SHALL be created with `create_engine(settings.DATABASE_URL)`.

#### Scenario: Engine created with SQLite URL
- **WHEN** `DATABASE_URL` starts with `sqlite://`
- **THEN** engine SHALL be created with `connect_args={"check_same_thread": False}`.

### Requirement: Session factory
The system SHALL provide a session factory for creating database sessions.

#### Scenario: `SessionLocal()` returns a session
- **WHEN** code calls `SessionLocal()`
- **THEN** it SHALL return a new `Session` instance bound to the engine.

#### Scenario: Session closed after use
- **WHEN** session context ends
- **THEN** the session SHALL be automatically closed.

### Requirement: Declarative base
The system SHALL provide a declarative base class for ORM models.

#### Scenario: Models inherit from Base
- **WHEN** a model class inherits from `Base`
- **THEN** it SHALL be registered with SQLAlchemy metadata.

### Requirement: FastAPI database dependency
The system SHALL provide a FastAPI dependency that yields database sessions.

#### Scenario: `get_db()` yields session
- **WHEN** an endpoint uses `Depends(get_db)`
- **THEN** it SHALL receive a database session that is closed after the request.

#### Scenario: Session closed after request
- **WHEN** request completes
- **THEN** the database session SHALL be closed.

### Requirement: Database tests
The system SHALL include tests for database connectivity and session management.

#### Scenario: Database connection test
- **WHEN** `test_database_connection` runs
- **THEN** it SHALL verify engine creation and basic connectivity.

#### Scenario: Session yields and closes
- **WHEN** `test_database_session` tests `get_db()`
- **THEN** it SHALL verify session is yielded and closed after use.