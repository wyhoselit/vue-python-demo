## ADDED Requirements

### Requirement: AI Endpoints
The system SHALL expose AI functionality via REST API.

#### Scenario: Chat completion
- **WHEN** user POSTs to `/api/v1/ai/chat` with messages and model
- **THEN** system returns completion (streaming or full)

#### Scenario: Embedding generation
- **WHEN** user POSTs to `/api/v1/ai/embeddings` with text
- **THEN** system returns vector embedding