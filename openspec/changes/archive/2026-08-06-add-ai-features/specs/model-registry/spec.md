## ADDED Requirements

### Requirement: Model Registry
The system SHALL manage and version AI models.

#### Scenario: Register new model
- **WHEN** user uploads a model config
- **THEN** system saves the model metadata and version

### Requirement: Model Selection
The system SHALL allow selecting specific model versions for inferences.

#### Scenario: Model switch
- **WHEN** user requests a model inferrence with a specific version
- **THEN** system uses that specific model version
