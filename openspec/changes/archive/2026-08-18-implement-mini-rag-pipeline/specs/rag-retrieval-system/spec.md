## ADDED Requirements

### Requirement: Retrieval System
The RAG pipeline SHALL retrieve the most relevant document chunks from the vector store based on a given user query.

#### Scenario: Retrieve relevant chunks for query
- **WHEN** a user query is provided to the retrieval system
- **THEN** the system SHALL return a ranked list of relevant document chunks.

#### Scenario: No relevant chunks found
- **WHEN** a user query does not yield relevant document chunks
- **THEN** the system SHALL return an empty list or a pre-defined fallback message.
