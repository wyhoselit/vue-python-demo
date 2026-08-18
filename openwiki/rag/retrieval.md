---
type: Concept
title: RAG Retrieval
description: Explains the retrieval mechanism for the Retrieval-Augmented Generation (RAG) pipeline, including similarity search and API endpoints.
tags: [RAG, retrieval, similarity search, API, backend]
resource: /backend/app/modules/llm/rag/retriever.py
---
# RAG Retrieval

The Retrieval component is responsible for finding the most relevant document chunks from the [Vector Store](vector_store.md) given a user's query. This is the core "search" step in the RAG pipeline.

## Components

### Retriever Logic (`retriever.py`)

The `retriever.py` module contains the core logic for performing similarity searches.

*   **`generate_query_embedding(query: str)`**: Converts the user's query string into an embedding using the same `EmbeddingGenerator` used during document ingestion (ensuring embedding space consistency).
*   **`retrieve(query: str, n_results: int = 5)`**: The main retrieval function. It embeds the query and queries the [Vector Store](vector_store.md) for the top `n_results` similar chunks.
*   **`retrieve_with_embedding(query_embedding: list[float], n_results: int = 5)`**: An alternative that accepts a pre-computed embedding, useful if the embedding is generated elsewhere or for testing.

*   **Source File**: `backend/app/modules/llm/rag/retriever.py`

### Retrieval API (`retrieval_service.py`)

The `retrieval_service.py` module exposes a FastAPI endpoint for the retrieval functionality.

*   **Endpoint**: `POST /retrieve`
*   **Request Body**: `RetrievalRequest` (contains `query: str` and optional `n_results: int`).
*   **Response**: Returns the raw results from the vector store query, including `ids`, `documents` (text content), `metadatas`, and `distances`.

*   **Source File**: `backend/app/modules/llm/rag/retrieval_service.py`

## Workflow

1.  User query is received (via API or internal call).
2.  Query is embedded using `EmbeddingGenerator`.
3.  Query embedding is used to search the ChromaDB collection via `VectorStore.query()`.
4.  Top-K matching document chunks (with text and metadata) are returned.
5.  These chunks are then passed to the [LLM Integration](llm_integration.md) to generate a grounded response.

## Configuration

*   The number of results (`n_results`) defaults to 5 but can be adjusted per request.
*   The similarity metric is determined by the ChromaDB collection configuration (default is typically cosine similarity).

## Dependencies

*   [Embedding Generation](embedding_generation.md) - for query embedding
*   [Vector Store](vector_store.md) - for storage and search