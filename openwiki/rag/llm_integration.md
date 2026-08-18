---
type: Concept
title: RAG LLM Integration
description: Details how Large Language Models (LLMs) are integrated into the RAG pipeline to generate context-aware responses.
tags: [RAG, LLM, prompt engineering, backend]
resource: /backend/app/modules/llm/rag/llm_integrator.py
---
# RAG LLM Integration

This module (`llm_integrator.py`) handles the integration of retrieved documents with the Large Language Model (LLM) to generate informed responses. It focuses on preparing the context for the LLM and constructing the final prompt.

## Components

### `format_context_for_llm(documents: List[Document]) -> str`
*   **Purpose**: Takes a list of `Document` objects (retrieved chunks) and formats them into a single, cohesive string suitable for insertion into an LLM prompt.
*   **Details**: Each document's `page_content` is appended, clearly labeled (e.g., "Document 1:"), with double newlines for separation.

### `generate_rag_prompt(query: str, context: str, template: str) -> str`
*   **Purpose**: Constructs the final prompt for the LLM by combining the user's `query`, the `context` string (from `format_context_for_llm`), and a predefined `template`.
*   **Details**: Uses Python's `str.format()` method to inject the context and query into placeholders within the `template`.

## Workflow

1.  After relevant documents are retrieved by the [Retrieval Service](retrieval.md), they are passed to `format_context_for_llm` to create a consolidated context string.
2.  The context string, along with the original user `query`, is then used by `generate_rag_prompt` to create a final, enriched prompt based on a RAG-specific template.
3.  This final prompt is then sent to the underlying LLM via the `LLMService` (defined in `app.modules.ai.services.llm_service.py`) for response generation.

## RAG Prompt Template

The `llm_service.py` module defines the default `RAG_PROMPT_TEMPLATE` used:

```
"""Use the following context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\n{context}\n\nQuestion: {query}\n\nAnswer:"""
```

This template guides the LLM to use the provided context and to avoid hallucination if the answer is not found within the context.

*   **Source File**: `backend/app/modules/llm/rag/llm_integrator.py`
*   **Dependency**: `backend/app/modules/ai/services/llm_service.py` (for the overall LLM interaction and prompt template definition)