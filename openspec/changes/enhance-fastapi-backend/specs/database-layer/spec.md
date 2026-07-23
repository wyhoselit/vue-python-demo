## ADDED Requirements

### Requirement: SQLAlchemy engine initialization
The system SHALL create a SQLAlchemy engine using the DATABASE_URL from configuration.

#### Scenario: Engine created with PostgreSQL URL
- **WHEN** DATABASE_URL starts with `postgresql://`
- **THEN** system SHALL create an engine configured for PostgreSQL

#### Scenario: Engine created with SQLite URL
- **WHEN** DATABASE_URL starts with `sqlite://`
- **THEN** system SHALL create an engine configured for SQLite

### Requirement: Session factory provided
The system SHALL provide a session factory for creating database sessions.

#### Scenario: Create new session
- **WHEN** code calls `SessionLocal()`
- **THEN** system SHALL return a new database session

#### Scenario: Session closed after use
- **WHEN** session context ends
- **THEN** system SHALL automatically close the session

### Requirement: Database dependency for FastAPI
The system SHALL provide a FastAPI dependency that yields database sessions.

#### Scenario: Dependency injects session
- **WHEN** endpoint uses `Depends(get_db)`
- **THEN** system SHALL inject a database session

#### Scenario: Session closed after request
- **WHEN** request completes
- **THEN** system SHALL close the database session

### Requirement: Base model class provided
The system SHALL provide a declarative base class for ORM models.

#### Scenario: Model inherits from Base
- **WHEN** model class inherits from `Base`
- **THEN** system SHALL register it with SQLAlchemy metadata
