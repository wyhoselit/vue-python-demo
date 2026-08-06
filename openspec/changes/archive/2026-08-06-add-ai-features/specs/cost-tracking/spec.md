## ADDED Requirements

### Requirement: Token Usage Tracking
The system SHALL track token usage per request and per user.

#### Scenario: Usage logging
- **WHEN** LLM request completes
- **THEN** system logs input/output tokens, model used, and user ID

### Requirement: Rate Limiting
The system SHALL enforce rate limits and daily budgets.

#### Scenario: Budget enforcement
- **WHEN** user exceeds daily token budget
- **THEN** system rejects subsequent requests with 429 status