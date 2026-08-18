# Vector Database: ChromaDB for Local Dev, PGVector for Production

## Context
The RAG pipeline needs a vector store for document embeddings. Two options were evaluated:
- **ChromaDB**: Local file-based, zero infrastructure, Python-native, simple API
- **PGVector**: PostgreSQL extension, ACID compliant, single database, existing infra

## Decision
Use **ChromaDB for local development and testing**, **PGVector for production deployment**.

## Rationale
- ChromaDB requires no additional infrastructure (no separate PostgreSQL with pgvector extension)
- Fast iteration in dev: no schema migrations, no connection pooling concerns
- PGVector leverages existing PostgreSQL investment: single backup/restore, ACID, existing connection pool
- Both support HNSW indexes for ANN search
- Migration path is clean: same embedding dimension (384), same metadata schema

## Consequences
- Dev environment differs from prod (vector store implementation)
- Need abstraction layer (`VectorStore` interface) to swap implementations
- CI must test against both or document limitation
- Production PostgreSQL needs `pgvector` extension enabled