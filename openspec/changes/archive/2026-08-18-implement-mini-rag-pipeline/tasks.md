## 1. Environment Setup & Dependencies

- [x] 1.1 Install ChromaDB Python client
- [x] 1.2 Install Sentence-Transformers library
- [x] 1.3 Install MLflow client
- [x] 1.4 Create `backend/app/modules/llm/rag/` directory structure
- [x] 1.5 Update `requirements.txt` or `pyproject.toml` with new dependencies

## 2. RAG Document Ingestion

- [x] 2.1 Implement document loader (e.g., for PDF, TXT) in `rag/document_loader.py`
- [x] 2.2 Implement text splitter for chunking documents in `rag/text_splitter.py`
- [x] 2.3 Create ingestion service endpoint/function in `rag/ingestion_service.py`

## 3. Embedding Generation

- [x] 3.1 Implement embedding model loading and inference in `rag/embedding_generator.py`
- [x] 3.2 Integrate embedding generation into ingestion service

## 4. Vector Store Integration

- [x] 4.1 Implement ChromaDB client initialization and connection in `rag/vector_store.py`
- [x] 4.2 Implement methods to add/retrieve embeddings from ChromaDB
- [x] 4.3 Integrate vector store operations into ingestion service

## 5. Retrieval System

- [x] 5.1 Implement query embedding generation for retrieval
- [x] 5.2 Implement similarity search against ChromaDB in `rag/retriever.py`
- [x] 5.3 Create retrieval service endpoint/function

## 6. LLM Generation with Context

- [x] 6.1 Implement context formatting for LLM prompts in `rag/llm_integrator.py`
- [x] 6.2 Modify existing LLM invocation to accept and utilize RAG context
- [x] 6.3 Create RAG query endpoint/function that orchestrates retrieval and LLM generation

## 7. Model Versioning & Experiment Tracking

- [x] 7.1 Implement MLflow tracking initialization
- [x] 7.2 Add MLflow logging for embedding model parameters and metrics during training/evaluation (if applicable)
- [x] 7.3 Add MLflow logging for RAG pipeline experiment parameters (e.g., chunk size, top-k retrieval) and LLM generation metrics
- [x] 7.4 Implement simple model registry for RAG components (e.g., embedding model path, ChromaDB instance)

## 8. Testing & Verification

- [x] 8.1 Write unit tests for document loaders and text splitter
- [x] 8.2 Write unit tests for embedding generation and vector store operations
- [x] 8.3 Write integration tests for retrieval and LLM generation with context
- [x] 8.4 Verify MLflow logging and model versioning functionality
