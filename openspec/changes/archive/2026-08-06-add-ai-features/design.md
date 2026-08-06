## Context

The current codebase is a FastAPI + Vue.js application with module-based architecture (`admin`, `system`, `user`, `dashboard`, `core`). It uses SQLAlchemy ORM, JWT authentication, and follows REST patterns. The system runs on Docker with PostgreSQL.

We need to add AI/ML capabilities without disrupting existing functionality. The AI features should be modular, provider-agnostic, and scalable.

## Goals / Non-Goals

**Goals:**
- Provider-agnostic LLM abstraction (OpenAI, Anthropic, local via Ollama)
- Vector search with pgvector (PostgreSQL extension) for RAG
- Async task queue for embedding generation and batch inference
- Model registry for versioning and A/B deployment
- Streaming chat/completion endpoints
- Chat interface for frontend
- Cost tracking and rate limiting

**Non-Goals:**
- Training infrastructure (use external services)
- Fine-tuning pipeline (out of scope for MVP)
- Multi-modal support (images, audio) - phase 2
- Custom model hosting (use Hugging Face / OpenAI APIs)

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| LLM Framework | `langchain` + custom provider abstraction | Battle-tested, supports streaming/function calling, easy to swap providers |
| Vector DB | `pgvector` (PostgreSQL extension) | No new infrastructure, already using PostgreSQL, ACID compliance |
| Task Queue | `dramatiq` + Redis | Simpler than Celery, integrates well with FastAPI, async support |
| Model Registry | JSONB in PostgreSQL + file storage | Simple to start, can migrate to MLflow later |
| Auth for AI endpoints | Reuse existing JWT + new `ai_access` scope | Consistent with existing auth system |
| Streaming | Server-Sent Events (SSE) | Native browser support, works with existing nginx/proxy |

## Risks / Trade-offs

- [Vendor Lock-in] → Mitigation: Abstract behind `LLMProvider` interface, implement adapters
- [pgvector Scale Limits] → Mitigation: Start with pgvector, plan migration to Weaviate/Qdrant if >1M vectors
- [Async Complexity] → Mitigation: Use dramatiq actors with clear retry/dead-letter policies
- [Cost Overruns] → Mitigation: Hard token limits per request + daily budget per user
- [Cold Start Latency] → Mitigation: Keep warm pools for common models, async pre-computation