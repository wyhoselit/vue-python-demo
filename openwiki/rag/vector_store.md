---
type: Concept
title: RAG Vector Store
description: Describes the ChromaDB-based vector store used for persisting and querying document embeddings in the RAG pipeline.
tags: [RAG, vector store, ChromaDB, backend]
resource: /backend/app/modules/llm/rag/vector_store.py
---
# RAG Vector Store

The Vector Store is the persistence layer for the RAG pipeline, responsible for storing document embeddings along with their associated text and metadata, and enabling efficient similarity search.

## Implementation

The `vector_store.py` module provides a wrapper around ChromaDB, a popular open-source vector database.

*   **ChromaDB**: Used as the underlying storage engine. It persists data to disk (by default in `./chroma_db`) and provides fast nearest-neighbor search.
*   **Singleton Pattern**: The module exposes a `get_vector_store` function that returns a singleton instance of the `VectorStore` class, ensuring a single connection pool to the database.

## `VectorStore` Class

**`__init__(self, persist_directory: str = "./chroma_db", collection_name: str = "rag_documents")`**
*   Initializes a `chromadb.PersistentClient` pointing to `persist_directory`.
*   Gets or creates a collection named `collection_name`.
*   Disables anonymized telemetry.

**`add_documents(self, documents: list[dict])`**
*   Adds a batch of documents to the collection.
*   Expected dictionary keys: `id`, `embedding`, `document` (the text content), `metadata`.

**`query(self, query_embedding: list[float], n_results: int = 5) -> dict`**
*   Performs a similarity search against the collection using the provided `query_embedding`.
*   Returns the top `n_results` matches, including their IDs, documents, metadata, and distances.

**`get_collection_info(self) -> dict`**
*   Returns basic info about the collection, such as its name and document count.

## Usage in RAG Pipeline

1.  After [Embedding Generation](embedding_generation.md), the [Ingestion Service](document_ingestion.md) calls `add_documents` to persist the embedded chunks.
2.  During a user query, the [Retrieval](retrieval.md) service calls `query` with the user's query embedding to find the most relevant document chunks.

*   **Source File**: `backend/app/modules/llm/rag/vector_store.py`
*   **Dependency**: `chromadb`