---
type: Overview
title: RAG Pipeline Overview
description: High-level overview of the Retrieval-Augmented Generation (RAG) pipeline implementation in the backend, covering document ingestion, embedding generation, vector storage, retrieval, LLM integration, and experiment tracking.
tags: [RAG, architecture, backend, AI]
resource: /backend/app/modules/llm/rag/
---
# RAG Pipeline Overview

The RAG (Retrieval-Augmented Generation) pipeline enhances the application's AI capabilities by allowing the LLM to access and reason over external knowledge sources. It is implemented in the `backend/app/modules/llm/rag/` directory.

## Architecture

The pipeline consists of the following main components, orchestrated by the `ingestion_service.py` and used by `llm_integrator.py`:

1.  **Document Ingestion** (`document_loader.py`, `text_splitter.py`): Loads documents (PDF, TXT) and splits them into overlapping chunks.
2.  **Embedding Generation** (`embedding_generator.py`): Uses a Sentence-Transformer model (`all-MiniLM-L6-v2` by default) to convert text chunks into vector embeddings.
3.  **Vector Store** (`vector_store.py`): Uses ChromaDB to persist and query document embeddings.
4.  **Retrieval** (`retrieval_service.py`, `retriever.py`): Performs similarity search against the vector store to find relevant document chunks for a given query.
5.  **LLM Integration** (`llm_integrator.py`): Combines retrieved context with the user query and sends it to the LLM service for generation.
6.  **Experiment Tracking** (`mlflow_tracker.py`): Logs experiments, parameters, and metrics to MLflow for reproducibility.

## Data Flow

1.  Documents are loaded and split into chunks.
2.  Chunks are embedded and stored in ChromaDB with metadata.
3.  User query is embedded and used to retrieve top-K similar chunks from ChromaDB.
4.  Retrieved chunks are formatted as context.
5.  Context + query is passed to the LLM via `llm_integrator.py` and `llm_service.py`.
6.  LLM generates a grounded response.
7.  (Optional) Pipeline steps and results are logged to MLflow.

## Key Files

| Component | File | Purpose |
|-----------|------|---------|
| Document Loading | `document_loader.py` | Load PDF/TXT files using LangChain loaders |
| Text Splitting | `text_splitter.py` | Split documents into overlapping chunks using `RecursiveCharacterTextSplitter` |
| Embeddings | `embedding_generator.py` | Generate vector embeddings using `sentence-transformers` |
| Vector Store | `vector_store.py` | ChromaDB wrapper for persistence and similarity search |
| Ingestion Orchestration | `ingestion_service.py` | Coordinates loading, splitting, embedding, and storing |
| Retrieval | `retrieval_service.py`, `retriever.py` | Query vector store for relevant context |
| LLM Integration | `llm_integrator.py` | Bridge between retrieval and LLM generation |
| Experiment Tracking | `mlflow_tracker.py` | MLflow integration for logging experiments |

## Related Pages

- [Document Ingestion](document_ingestion.md) -> details the loading and splitting process
- [Embedding Generation](embedding_generation.md) -> covers the embedding model and generation
- [Vector Store](vector_store.md) -> explains ChromaDB integration and persistence
- [Retrieval](retrieval.md) -> describes similarity search and context retrieval
- [LLM Integration](llm_integration.md) -> shows how retrieved context is used for generation
- [Experiment Tracking](experiment_tracking.md) -> covers MLflow logging