import chromadb
from chromadb.config import Settings

from app.modules.ai.services.vector_store import SearchResult, VectorStore


class ChromaVectorStore(VectorStore):
    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        collection_name: str = "rag_documents",
    ):
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(name=collection_name)

    async def add_documents(self, documents: list[dict]) -> None:
        ids = [doc["id"] for doc in documents]
        embeddings = [doc["embedding"] for doc in documents]
        texts = [doc["document"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )

    async def search(
        self,
        query_embedding: list[float],
        limit: int = 10,
        filter_metadata: dict | None = None,
    ) -> list[SearchResult]:
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where=filter_metadata,
        )

        return [
            SearchResult(
                id=result["ids"][0][i],
                text=result["documents"][0][i],
                score=1.0 - result["distances"][0][i] if result["distances"] else 0.0,
                metadata=result["metadatas"][0][i] or {},
            )
            for i in range(len(result["ids"][0]))
        ]

    async def delete(self, ids: list[str]) -> None:
        self.collection.delete(ids=ids)

    async def health_check(self) -> bool:
        try:
            self.collection.count()
            return True
        except Exception:  # noqa: BLE001
            return False

    def get_collection_info(self) -> dict:
        return {"name": self.collection.name, "count": self.collection.count()}
