---
type: Concept
title: RAG Document Ingestion
description: Details the process of loading and splitting documents into manageable chunks for the Retrieval-Augmented Generation (RAG) pipeline.
tags: [RAG, document processing, ingestion, backend]
resource: /backend/app/modules/llm/rag/ingestion_service.py
---
# RAG Document Ingestion

Document ingestion is the initial step in the RAG pipeline, responsible for preparing raw documents for embedding and storage. This process involves loading documents from various formats and splitting them into smaller, overlapping chunks.

## Components

### Document Loader

The `document_loader.py` module handles reading different document types. It currently supports:

*   **PDF files**: Utilizes `PyPDFLoader` from `langchain_community`.
*   **Text files (.txt)**: Utilizes `TextLoader` from `langchain_community`.

If an unsupported file type is encountered, it raises a `ValueError`. The `load_documents_from_directory` function allows for batch processing of files within a given directory.

*   **Source File**: `backend/app/modules/llm/rag/document_loader.py`

### Text Splitter

The `text_splitter.py` module is responsible for breaking down large documents into smaller, more manageable `Document` objects. This is crucial because embedding models often have input token limits, and smaller chunks allow for more precise retrieval.

It uses LangChain's `RecursiveCharacterTextSplitter`, which attempts to split text using a list of characters until chunks are small enough. It also supports configurable `chunk_size` and `chunk_overlap` to maintain context across splits.

*   **Source File**: `backend/app/modules/llm/rag/text_splitter.py`

### Ingestion Service

The `ingestion_service.py` module orchestrates the entire document ingestion process. It ties together the document loading and text splitting steps, and also facilitates the generation of embeddings and storage into the vector store.

Key functions include:

*   `ingest_document`: Processes a single file.
*   `ingest_documents_from_directory`: Processes all supported files in a given directory.
*   `ingest_and_store_document` (async):
*   `ingest_and_store_documents_from_directory` (async): These functions not only ingest but also generate embeddings and store the resulting chunks in the [Vector Store](vector_store.md).

*   **Source File**: `backend/app/modules/llm/rag/ingestion_service.py`

## Workflow

1.  A document path or directory path is provided to the `ingestion_service`.
2.  `document_loader` reads the raw content.
3.  `text_splitter` divides the content into chunks.
4.  Each chunk is then passed to the [Embedding Generation](embedding_generation.md) process.
5.  Finally, the embedded chunks are stored in the [Vector Store](vector_store.md).