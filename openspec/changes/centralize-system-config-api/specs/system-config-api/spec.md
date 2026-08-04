## ADDED Requirements

### Requirement: Centralized System Configuration API
The system SHALL provide endpoints to get, set, and delete dynamic configurations stored in the `system_settings` table. This includes configuration keys for: `tracing.admin`, `system.logfile_path`, and any future system-level settings.

#### Scenario: Get configuration by key
- **WHEN** admin requests `GET /api/v1/system/config/{key}`
- **THEN** system returns the JSON value associated with the key

#### Scenario: Update configuration value
- **WHEN** admin requests `PUT /api/v1/system/config/{key}` with payload
- **THEN** system updates the value in the `system_settings` table

### Requirement: System Logfile Path Configuration
The system SHALL provide a `system.logfile_path` configuration that allows specifying the path to the application logfile.

#### Scenario: Get logfile path configuration
- **WHEN** admin requests `GET /api/v1/system/config/system.logfile_path`
- **THEN** system returns the configured logfile path or a default path if not set

#### Scenario: Update logfile path configuration
- **WHEN** admin requests `PUT /api/v1/system/config/system.logfile_path` with `{"path": "/var/log/app.log"}`
- **THEN** system updates the logfile path in the `system_settings` table and applies the new path to the logging configuration
