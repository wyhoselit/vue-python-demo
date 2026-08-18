from app.modules.llm.rag.embedding_generator import EmbeddingGenerator
from app.modules.llm.rag.vector_store import get_vector_store


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


def retrieve(query: str, n_results: int = 5) -> dict:
    """
    Performs similarity search against the vector store using a query string.

    Args:
        query: The query string to search for.
        n_results: Number of results to return.

    Returns:
        Dictionary with keys: 'ids', 'documents', 'metadatas', 'distances'
    """
    query_embedding = generate_query_embedding(query)
    vector_store = get_vector_store()
    return vector_store.query(query_embedding, n_results)


def retrieve_with_embedding(query_embedding: list[float], n_results: int = 5) -> dict:
    """
    Performs similarity search against the vector store using a pre-computed embedding.

    Args:
        query_embedding: The pre-computed query embedding.
        n_results: Number of results to return.

    Returns:
        Dictionary with keys: 'ids', 'documents', 'metadatas', 'distances'
    """
    vector_store = get_vector_store()
    return vector_store.query(query_embedding, n_results)