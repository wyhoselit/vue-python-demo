## Why

The current codebase is a well-structured FastAPI + Vue.js application with clear module separation (admin, system, user, dashboard, core). However, it lacks native AI/ML integration capabilities. To fulfill the "人工智慧平台開發" (AI platform development) requirement from the job spec, we need to add LLM integration, vector search, and model serving infrastructure.

## What Changes

- Add LLM abstraction layer with provider-agnostic interface (OpenAI, Anthropic, local models)
- Implement vector database integration (pgvector/Weaviate) for RAG capabilities
- Add async task queue for long-running AI workloads (embeddings, batch inference)
- Create model registry for versioning and A/B testing
- Add streaming response support for chat/completion endpoints
- Implement cost tracking and rate limiting per user/tenant

## Capabilities

### New Capabilities
- `llm-gateway`: Unified LLM provider abstraction with streaming, function calling, and structured output support
- `vector-search`: Embedding generation, vector storage, and similarity search for RAG
- `model-registry`: Model versioning, metadata, and deployment management
- `ai-task-queue`: Async job processing for embeddings, fine-tuning, batch inference
- `cost-tracking`: Token usage monitoring, rate limiting, and billing integration

### Modified Capabilities
- `backend-api`: Extended with new AI endpoints under `/api/v1/ai/`
- `system-config`: Extended to manage AI provider keys, model configs, and feature flags

## Impact

- **Backend**: New modules `ai/` and `vector/` under `app/modules/`
- **Frontend**: New modules `ai/` under `frontend/src/modules/` for chat UI, model playground
- **Database**: New tables for conversations, embeddings, model metadata, usage logs
- **Infrastructure**: Requires Redis for task queue, pgvector extension or Weaviate instance
- **Dependencies**: Add `langchain`, `openai`, `anthropic`, `pgvector`, `celery`/`dramatiq`