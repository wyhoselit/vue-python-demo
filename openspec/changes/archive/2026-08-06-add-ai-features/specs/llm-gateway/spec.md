## ADDED Requirements

### Requirement: LLM Gateway
The system SHALL provide a unified API interface for LLM operations.

#### Scenario: Completion request
- **WHEN** user requests a text completion with a model key
- **THEN** system returns the generated completion using the selected provider

#### Scenario: Streaming response
- **WHEN** user requests a streaming completion
- **THEN** system returns the response via Server-Sent Events (SSE)

### Requirement: Provider Abstraction
The system SHALL allow switching between LLM providers without frontend changes.

#### Scenario: Provider swap
- **WHEN** administrator updates the active provider in system config
- **THEN** subsequent completion requests are routed to the new provider
