# API Module Architecture: Modular Monolith with Clear Boundaries

## Context
The backend currently uses a modular structure under `backend/app/modules/` (user, ai, admin, system, dashboard). There's no clear data boundary pattern - all modules share the same PostgreSQL database via the core `database.py`.

## Decision
Architect as a **modular monolith** with **explicit data boundaries**:
- One database instance (PostgreSQL with pgvector extension)
- Module boundaries enforced in code, not database
- Synchronous communication via direct function calls
- Authentication via FastAPI dependencies

## Rationale
- Simpler deployment (single container vs multiple services)
- Transactional consistency across modules
- No network latency for inter-module calls
- Single backup/restore process
- Fits current team size and deployment model (K8s single backend deployment)

## Consequences
- Horizontal scaling limited to API replicas (shared database is bottleneck)
- Database becomes single point of failure
- Module changes risk affecting entire system
- Future evolution to microservices requires careful database splitting