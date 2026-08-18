## Context

The `backend/app/modules/llm/` directory currently exists but lacks a full RAG pipeline. This design introduces a mini RAG pipeline to enable LLM responses augmented with external knowledge, plus model versioning and experiment tracking.

## Goals / Non-Goals

**Goals:**
- Implement a functional RAG pipeline: ingestion → embedding → vector store → retrieval → generation.
- Add model versioning for RAG/LLM configurations.
- Add experiment tracking for RAG/LLM development.

**Non-Goals:**
- Full production-grade MLOps platform (e.g., Kubeflow pipelines).
- Multi-modal RAG (images, audio).
- Distributed vector search at massive scale.

## Decisions

1. **Vector Store**: **ChromaDB** (local, simple, Python-native). Alternative: PGVector (requires Postgres). Reason: minimal infra, good for "mini" scope.
2. **Embedding Model**: **Sentence-Transformers (all-MiniLM-L6-v2)**. Alternative: OpenAI embeddings. Reason: local, no API cost, good baseline.
3. **LLM Integration**: Use existing `backend/app/modules/llm/` patterns; wrap RAG context into prompt.
4. **Experiment Tracking**: **MLflow** (local tracking server). Alternative: Weights & Biases, ClearML. Reason: open-source, integrates with Python, model registry support.
5. **Pipeline Orchestration**: Simple Python classes/functions (no Airflow/Prefect). Reason: "mini" scope, keep deps low.

## Risks / Trade-offs

- [ChromaDB local persistence] → Mitigation: configure persistent directory; document backup/restore.
- [Embedding model quality] → Mitigation: allow swapping embedding model via config; benchmark alternatives.
- [MLflow local server ops] → Mitigation: provide docker-compose for dev; document startup.
- [No async/parallel ingestion] → Mitigation: scope as future improvement; design ingestion interface for extensibility.