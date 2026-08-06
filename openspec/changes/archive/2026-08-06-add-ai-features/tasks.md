## 1. Setup

- [x] 1.1 Create ai/ and vector/ module directories
- [x] 1.2 Configure Redis for async task queue
- [x] 1.3 Add dependencies: langchain, openai, anthropic, pgvector, dramatiq

## 2. Core Implementation

- [x] 2.1 Implement LLMProvider interface and OpenAI/Anthropic/Local adapters
- [x] 2.2 Configure FastAPI endpoints under /api/v1/ai/
- [x] 2.3 Implement vector search service with pgvector
- [x] 2.4 Create dramatiq actors for embedding and batch inference

## 3. Registry & Monitoring

- [x] 3.1 Implement ModelRegistry using JSONB storage
- [x] 3.2 Add cost tracking middleware for token usage
- [x] 3.3 Add rate limiting per user
- [x] 3.4 Implement SSE streaming for chat endpoints

## 4. Frontend

- [x] 4.1 Create Chat page component with message history and input
- [x] 4.2 Add chat route and navigation
- [x] 4.3 Implement SSE streaming display for responses

## 5. Testing

- [x] 5.1 Add unit tests for ChatView component
- [x] 5.2 Add unit tests for AI API service
