## ADDED Requirements

### Requirement: Backend unit tests can be executed
The system SHALL provide a mechanism to run unit tests for backend components.

#### Scenario: Pytest command runs successfully
- **WHEN** `pytest` is executed in the `backend/` directory
- **THEN** all defined unit tests SHALL pass without errors.

### Requirement: Configuration loading is tested
The system SHALL have unit tests for the `app.core.config` module.

#### Scenario: Default settings loaded
- **WHEN** `settings` is instantiated without `.env` file
- **THEN** default values (e.g., `DEBUG=False`) SHALL be correctly loaded.

#### Scenario: Environment variables override settings
- **WHEN** `.env` file with `DEBUG=True` is present
- **THEN** `settings.DEBUG` SHALL be `True`.

### Requirement: Database connection setup is tested
The system SHALL have unit tests for the `app.core.database` module.

#### Scenario: Engine creation with default URL
- **WHEN** `create_engine` is called with `settings.DATABASE_URL`
- **THEN** an SQLAlchemy engine SHALL be successfully created.

#### Scenario: SessionLocal provides a session
- **WHEN** `SessionLocal()` is invoked
- **THEN** a database session object SHALL be returned.
