# Backend Core Configuration Specification

## Purpose
Defines the centralized configuration management using Pydantic Settings with environment variable loading and validation.

## Requirements

### Requirement: Settings class with required configuration parameters
The system SHALL provide a `Settings` class that exposes all required configuration parameters.

#### Scenario: Settings object instantiated
- **WHEN** `Settings()` is instantiated
- **THEN** it SHALL have the following attributes:
  - `DATABASE_URL`: string with default `"sqlite:///./app.db"`
  - `SECRET_KEY`: string with default `"change-me-in-production"`
  - `DEBUG`: boolean with default `False`
  - `CORS_ORIGINS`: string with default `"http://localhost:5173"`
  - `API_V1_PREFIX`: string with default `"/api/v1"`

#### Scenario: Environment variables override defaults
- **WHEN** `.env` file contains `DATABASE_URL=postgresql://user:pass@localhost/db`
- **THEN** `settings.DATABASE_URL` SHALL equal `"postgresql://user:pass@localhost/db"`

#### Scenario: Invalid configuration raises error
- **WHEN** `DEBUG="invalid"` is provided
- **THEN** instantiation SHALL raise a validation error

### Requirement: Settings singleton instance
The system SHALL provide a module-level `settings` instance for import across the application.

#### Scenario: Settings imported and used
- **WHEN** code executes `from app.core.config import settings`
- **THEN** `settings` SHALL be a `Settings` instance with validated configuration

### Requirement: Configuration accessible in other modules
The configuration SHALL be accessible to database, CORS middleware, and API versioning modules.

#### Scenario: CORS middleware uses settings
- **WHEN** `main.py` configures `CORSMiddleware`
- **THEN** it SHALL use `settings.CORS_ORIGINS.split(",")` for `allow_origins`

#### Scenario: API router uses settings
- **WHEN** `main.py` includes `api_router`
- **THEN** it SHALL use `settings.API_V1_PREFIX` as prefix

#### Scenario: Database uses settings
- **WHEN** `database.py` creates engine
- **THEN** it SHALL use `settings.DATABASE_URL`