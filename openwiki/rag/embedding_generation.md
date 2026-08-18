---
type: Concept
title: RAG Embedding Generation
description: Explains how text chunks are converted into numerical vector embeddings for the Retrieval-Augmented Generation (RAG) pipeline.
tags: [RAG, embeddings, LLM, backend]
resource: /backend/app/modules/llm/rag/embedding_generator.py
---
# RAG Embedding Generation

Embedding generation is a critical step in the RAG pipeline where textual data (document chunks) is transformed into numerical vectors (embeddings). These embeddings capture the semantic meaning of the text, allowing for efficient similarity searches.

## Implementation

The `embedding_generator.py` module handles the creation of these embeddings.

*   It utilizes the `sentence-transformers` library, which provides pre-trained models for generating high-quality sentence and text embeddings.
*   By default, it uses the `all-MiniLM-L6-v2` model, a lightweight yet effective model suitable for many general-purpose embedding tasks.

## `EmbeddingGenerator` Class

**`__init__(self, model_name: str = 'all-MiniLM-L6-v2')`**
*   Initializes the `SentenceTransformer` model with the specified `model_name`.

**`generate_embedding(self, text: str)`**
*   Takes a single string (`text`) and returns its corresponding embedding as a list of floats.

**`generate_embeddings(self, texts: list[str])`**
*   Takes a list of strings (`texts`) and returns a list of embeddings, one for each input text.

## Usage in RAG Pipeline

Once documents are split into chunks by the [Document Ingestion](document_ingestion.md) service, these chunks are passed to the `EmbeddingGenerator` to produce their embeddings. These embeddings are then stored alongside the original text in the [Vector Store](vector_store.md) for later retrieval.

*   **Source File**: `backend/app/modules/llm/rag/embedding_generator.py`
