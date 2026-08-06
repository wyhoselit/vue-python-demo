## ADDED Requirements

### Requirement: AI Configuration Management
The system SHALL manage AI provider keys and model configurations via the system config API.

#### Scenario: Provider key storage
- **WHEN** admin sets an API key for a provider
- **THEN** system securely stores the encrypted key

#### Scenario: Default model configuration
- **WHEN** admin sets a default model
- **THEN** system uses this model as fallback when none specified