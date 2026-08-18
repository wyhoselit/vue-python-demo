---
type: Documentation Plan
title: RAG Pipeline Documentation Plan
description: Plan for documenting the new Retrieval Augmented Generation (RAG) pipeline components and their integration.
tags: [planning, RAG, documentation]
---
# RAG Pipeline Documentation Plan

## Intended Wiki Pages and Relationships

*   **`/openwiki/rag/overview.md`**:
    *   **Source Evidence**: `backend/app/modules/llm/rag/` directory structure, `backend/app/modules/ai/api/chat.py`, `backend/app/modules/ai/services/llm_service.py`
    *   **Relationships**:
        *   `overview.md` -> provides high-level explanation for -> `document_ingestion.md`
        *   `overview.md` -> provides high-level explanation for -> `embedding_generation.md`
        *   `overview.md` -> provides high-level explanation for -> `vector_store.md`
        *   `overview.md` -> provides high-level explanation for -> `retrieval.md`
        *   `overview.md` -> provides high-level explanation for -> `llm_integration.md`
        *   `overview.md` -> provides high-level explanation for -> `experiment_tracking.md`

*   **`/openwiki/rag/document_ingestion.md`**:
    *   **Source Evidence**: `backend/app/modules/llm/rag/document_loader.py`, `backend/app/modules/llm/rag/text_splitter.py`, `backend/app/modules/llm/rag/ingestion_service.py`
    *   **Relationships**:
        *   `document_ingestion.md` -> uses -> `document_loader.py`
        *   `document_ingestion.md` -> uses -> `text_splitter.py`
        *   `document_ingestion.md` -> orchestrates -> `ingestion_service.py`

*   **`/openwiki/rag/embedding_generation.md`**:
    *   **Source Evidence**: `backend/app/modules/llm/rag/embedding_generator.py`
    *   **Relationships**:
        *   `embedding_generation.md` -> implemented by -> `embedding_generator.py`

*   **`/openwiki/rag/vector_store.md`**:
    *   **Source Evidence**: `backend/app/modules/llm/rag/vector_store.py`
    *   **Relationships**:
        *   `vector_store.md` -> implemented by -> `vector_store.py`
        *   `vector_store.md` -> leverages -> `ChromaDB`

*   **`/openwiki/rag/retrieval.md`**:
    *   **Source Evidence**: `backend/app/modules/llm/rag/retrieval_service.py`, `backend/app/modules/llm/rag/retriever.py`
    *   **Relationships**:
        *   `retrieval.md` -> implemented by -> `retrieval_service.py`
        *   `retrieval.md` -> uses -> `retriever.py`
        *   `retrieval.md` -> queries -> `vector_store.md`

*   **`/openwiki/rag/llm_integration.md`**:
    *   **Source Evidence**: `backend/app/modules/llm/rag/llm_integrator.py`, `backend/app/modules/ai/services/llm_service.py`, `backend/app/modules/ai/api/chat.py`
    *   **Relationships**:
        *   `llm_integration.md` -> implemented by -> `llm_integrator.py`
        *   `llm_integration.md` -> integrates with -> `llm_service.py`
        *   `llm_integration.md` -> exposed via -> `chat.py` API

*   **`/openwiki/rag/experiment_tracking.md`**:
    *   **Source Evidence**: `backend/app/modules/llm/rag/mlflow_tracker.py`
    *   **Relationships**:
        *   `experiment_tracking.md` -> implemented by -> `mlflow_tracker.py`
        *   `experiment_tracking.md` -> leverages -> `MLflow`

## Updates to Existing Pages

*   **`/openwiki/backend-service.md`**:
    *   **Change**: Add a section on RAG integration, linking to `/openwiki/rag/overview.md`. Mention how RAG enhances the backend's AI capabilities.

*   **`/openwiki/quickstart.md`**:
    *   **Change**: Review for any impact of RAG on setup or usage. If RAG requires specific environment variables or setup steps, add a concise note and link to more detailed RAG documentation.

*   **`/openwiki/index.md`**:
    *   **Change**: Add a link to the new "RAG Pipeline" section, pointing to `/openwiki/rag/overview.md`.

*   **`/openwiki/observability.md`**:
    *   **Change**: Update with details from `frontend/src/modules/core/observability.ts`, `frontend/src/modules/core/router-observability.ts`, and `frontend/src/modules/core/tests/observability.spec.ts` if there are significant changes, especially related to the moved OpenTelemetry specs.

*   **`/openwiki/frontend-app.md`**:
    *   **Change**: Update to include information about the `ApexChart.vue` component and `docs/research/vue-charting-libraries.md`, reflecting the dashboard changes. Mention package-lock.json and package.json updates.

## Remaining Questions

*   Are there any specific configuration details for ChromaDB or the embedding model that should be documented in `vector_store.md` or `embedding_generation.md`?
*   Are there any environment variables related to RAG that need to be explicitly mentioned in quickstart or a dedicated config page?
*   How deeply should the MLflow tracking be explained, or is a high-level overview sufficient for `experiment_tracking.md`?
