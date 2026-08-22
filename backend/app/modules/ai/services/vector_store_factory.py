"""Vector store factory for dependency injection.

Provides a singleton pattern for vector store instances based on
configuration. Used for dependency injection in FastAPI endpoints.
"""

from app.modules.ai.services.vector_store import VectorStore
from app.modules.core.config import settings

_vector_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        if settings.VECTOR_STORE == "pgvector":
            from app.modules.ai.services.pgvector_store import PGVectorStore

            _vector_store = PGVectorStore()
        elif settings.VECTOR_STORE == "chroma":
            from app.modules.ai.services.chroma_vector_store import ChromaVectorStore

            _vector_store = ChromaVectorStore()
        else:
            raise ValueError(f"Unknown VECTOR_STORE: {settings.VECTOR_STORE}")
    return _vector_store


def reset_vector_store() -> None:
    """Reset the singleton for testing purposes."""
    global _vector_store
    _vector_store = None
