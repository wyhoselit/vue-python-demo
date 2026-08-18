import asyncio
from typing import Optional

from app.modules.ai.services.vector_store_factory import get_vector_store
from app.modules.llm.rag.embedding_generator import EmbeddingGenerator


_embedding_generator = EmbeddingGenerator()


def generate_query_embedding(query: str) -> list[float]:
    """
    Generates an embedding for a query string.

    Args:
        query: The query string to embed.

    Returns:
        The query embedding as a list of floats.
    """
    return _embedding_generator.generate_embedding(query)


async def retrieve(
    query: str,
    n_results: int = 5,
    filter_metadata: Optional[dict] = None,
) -> dict:
    """
    Performs similarity search against the vector store using a query string.

    Args:
        query: The query string to search for.
        n_results: Number of results to return.

    Returns:
        Dictionary with keys: 'ids', 'documents', 'metadatas', 'distances'
        (converted from SearchResult objects for backward compatibility)
    """
    query_embedding = generate_query_embedding(query)
    vector_store = get_vector_store()
    results = await vector_store.search(query_embedding, n_results, filter_metadata)

    return {
        "ids": [[r.id for r in results]],
        "documents": [[r.text for r in results]],
        "metadatas": [[r.metadata for r in results]],
        "distances": [[1.0 - r.score for r in results]],
    }


async def retrieve_with_embedding(
    query_embedding: list[float],
    n_results: int = 5,
    filter_metadata: Optional[dict] = None,
) -> dict:
    """
    Performs similarity search against the vector store using a pre-computed embedding.

    Args:
        query_embedding: The pre-computed query embedding.
        n_results: Number of results to return.

    Returns:
        Dictionary with keys: 'ids', 'documents', 'metadatas', 'distances'
        (converted from SearchResult objects for backward compatibility)
    """
    vector_store = get_vector_store()
    results = await vector_store.search(query_embedding, n_results, filter_metadata)

    return {
        "ids": [[r.id for r in results]],
        "documents": [[r.text for r in results]],
        "metadatas": [[r.metadata for r in results]],
        "distances": [[1.0 - r.score for r in results]],
    }