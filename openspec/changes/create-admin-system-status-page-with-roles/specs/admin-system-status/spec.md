## ADDED Requirements

### Requirement: System status API
The system SHALL expose an API endpoint for retrieving system information, including version, OS, and database connectivity status.

#### Scenario: Admin retrieves system status
- **WHEN** admin user calls GET `/api/v1/admin/system-info`
- **THEN** system SHALL return the system overview information

### Requirement: Application log retrieval
The system SHALL allow admin users to view recent application logs.

#### Scenario: Admin retrieves recent logs
- **WHEN** admin user calls GET `/api/v1/admin/logs`
- **THEN** system SHALL return the most recent log entries (e.g., last 100 lines)
