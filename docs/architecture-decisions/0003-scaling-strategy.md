# Scalability Strategy: Database-Centric with Horizontal API Scaling

## Context
The system handles RAG queries with LLM calls, user management, and admin functions. Expected load: 10k+ RPS, 1M+ documents.

## Decision
Implement **database-centric scalability** with the following patterns:

1. **API Layer**: Horizontal pod autoscaling (HPA) based on CPU/memory
   - Target: 70% CPU utilization
   - Min: 2 replicas, Max: 10

2. **Database Layer**: 
   - Read replicas for query-heavy workloads (RAG retrieval)
   - Connection pooling via SQLAlchemy (pool_size=10, max_overflow=20)
   - Partitioning for large document tables (by date/category)

3. **Vector Store**: 
   - PGVector with HNSW index (sub-linear ANN search)
   - Index parameters: m=16, ef_construction=64

4. **Rate Limiting**: 
   - Per-user LLM token limits
   - Global RPS limits per endpoint

## Rationale
- PostgreSQL handles ~5k RPS with proper tuning
- Read replicas offload search queries
- Vector similarity search is compute-heavy, needs local caching
- LLM costs scale with usage, rate limiting protects budget

## Consequences
- Database is the primary bottleneck
- Vector store needs separate caching layer at scale
- LLM inference latency dominates response time
- Future: consider separate LLM worker queue for async generation