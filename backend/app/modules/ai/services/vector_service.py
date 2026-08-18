from sentence_transformers import SentenceTransformer

from app.modules.ai.services.vector_store_factory import get_vector_store


class VectorService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self._model = SentenceTransformer(model_name)

    async def generate_embedding(
        self, text: str, model: str = "all-MiniLM-L6-v2"
    ) -> list[float]:
        return self._model.encode(text).tolist()

    async def store_embedding(
        self,
        id: str,
        text: str,
        embedding: list[float],
        metadata: dict | None = None,
    ) -> None:
        vector_store = get_vector_store()
        await vector_store.add_documents(
            [{"id": id, "document": text, "embedding": embedding, "metadata": metadata}]
        )

    async def search(self, query_embedding: list[float], limit: int = 10) -> list:
        vector_store = get_vector_store()
        return await vector_store.search(query_embedding, limit)
