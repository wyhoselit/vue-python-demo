from sentence_transformers import SentenceTransformer

from app.modules.ai.services.vector_store_factory import get_vector_store


class VectorService:
    """Service for generating embeddings and managing vector storage.

    Args:
        model_name: SentenceTransformer model to use for embedding generation.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self._model = SentenceTransformer(model_name)

    async def generate_embedding(
        self, text: str, model: str = "all-MiniLM-L6-v2"
    ) -> list[float]:
        """Generate a vector embedding for the given text.

        Args:
            text: Input text to embed.
            model: Model identifier (currently unused, reserved for future multi-model support).

        Returns:
            List of floats representing the embedding vector.
        """
        return self._model.encode(text).tolist()

    async def store_embedding(
        self,
        id: str,
        text: str,
        embedding: list[float],
        metadata: dict | None = None,
    ) -> None:
        """Store a text embedding in the vector store.

        Args:
            id: Unique identifier for the document.
            text: Original text content.
            embedding: Pre-computed embedding vector.
            metadata: Optional metadata to attach to the document.
        """
        vector_store = get_vector_store()
        await vector_store.add_documents(
            [{"id": id, "document": text, "embedding": embedding, "metadata": metadata}]
        )

    async def search(self, query_embedding: list[float], limit: int = 10) -> list:
        """Search the vector store for similar documents.

        Args:
            query_embedding: Query vector to search against.
            limit: Maximum number of results to return.

        Returns:
            List of matching documents sorted by similarity.
        """
        vector_store = get_vector_store()
        return await vector_store.search(query_embedding, limit)
