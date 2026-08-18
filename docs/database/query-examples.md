# Database Query Optimization Examples

This document demonstrates SQL and SQLAlchemy query optimization patterns implemented in the project, addressing common relational database bottlenecks.

---

## 1. N+1 Query Problem (Eager Loading)

### Scenario
Retrieving users along with their roles.

### 🛑 Unoptimized (Naive ORM Access)
Iterating over a collection of users and accessing `user.roles` dynamically triggers a new SQL query for each user.
```python
# Generates 1 query to fetch users + N queries to fetch roles for each user
db = SessionLocal()
users = db.query(User).all()
for user in users:
    role_names = [role.name for role in user.roles]  # N query triggers here
```

### 🚀 Optimized (Eager Loading via Joined Load)
Pre-fetching roles in a single query using a SQL `LEFT OUTER JOIN`.
```python
from sqlalchemy.orm import joinedload

# Generates exactly 1 SQL query using a JOIN
users = db.query(User).options(joinedload(User.roles)).all()
for user in users:
    role_names = [role.name for role in user.roles]  # No additional queries
```

---

## 2. Unstructured Data Search (JSONB Indexing & Querying)

### Scenario
Querying system configuration keys nested deep inside the `system_settings` JSON column.

### 🛑 Unoptimized (Sequential Scan)
Querying JSON fields without indexes forces a full table sequential scan (O(N)).
```python
# Raw query scan
settings = db.query(SystemSetting).filter(
    SystemSetting.settings['tracing']['enabled'].astext == 'true'
).all()
```

### 🚀 Optimized (GIN Indexing & Containment Operator)
Using PostgreSQL's JSONB type with a **GIN (Generalized Inverted Index)** allows indexing keys and values inside the document.

#### Database Index Creation (Alembic / SQL)
```sql
CREATE INDEX idx_system_settings_jsonb_gin ON system_settings USING gin (settings);
```

#### SQLAlchemy Optimized Query
Using the containment (`has_key` or `contains`) operator which utilizes the GIN index:
```python
# Uses GIN index for O(log N) lookup
settings = db.query(SystemSetting).filter(
    SystemSetting.settings.contains({"tracing": {"enabled": True}})
).all()
```

---

## 3. Vector Similarity Search (PGVector HNSW Index)

### Scenario
Retrieving the top $K$ documents nearest to a user's query embedding.

### 🛑 Unoptimized (Flat L2/Cosine Distance Scan)
Calculating cosine similarity against all rows (exact nearest neighbor search) is extremely expensive on large collections (requires computing distances for 100% of rows).
```python
# Exact search (O(N)), slow on >100k records
query_embedding = [...] # 384-dimension list
nearest_docs = db.query(Document).order_by(
    Document.embedding.cosine_distance(query_embedding)
).limit(5).all()
```

### 🚀 Optimized (HNSW Index & Approximate Nearest Neighbor)
Using the **HNSW (Hierarchical Navigable Small World)** index for sub-linear approximate nearest neighbor (ANN) search.

#### Database Index Creation (Alembic / SQL)
Creating the HNSW index on the vector embedding column using cosine distance:
```sql
CREATE INDEX idx_documents_embedding_hnsw ON documents 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 64);
```

#### SQLAlchemy Optimized Query
```python
# Approximate nearest neighbor search utilizing the HNSW index
nearest_docs = db.query(Document).order_by(
    Document.embedding.cosine_distance(query_embedding)
).limit(5).all()
```

---

## 4. Read Replica Architecture Readiness

To route queries dynamically between a Primary (Write) database and multiple Read-only Replicas, we can configure a routing engine session in SQLAlchemy.

### Implementation Blueprint (`backend/app/core/database.py`)
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None):
        # Route write operations (insert/update/delete) to Primary
        if self._flushing or (clause is not None and not clause.is_select):
            return engines['writer']
        # Route read operations (select) to Replica
        return engines['reader']

engines = {
    'writer': create_engine(settings.DATABASE_WRITE_URL, pool_size=10, max_overflow=20),
    'reader': create_engine(settings.DATABASE_READ_URL, pool_size=15, max_overflow=30)
}

SessionLocal = sessionmaker(class_=RoutingSession, autocommit=False, autoflush=False)
```
