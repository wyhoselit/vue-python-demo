"""Vector store interface for embedding storage and retrieval.

Abstract base class defining the contract for vector database
implementations (Chroma, PGVector, etc.).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SearchResult:
    id: str
    text: str
    score: float
    metadata: dict


class VectorStore(ABC):
    @abstractmethod
    async def add_documents(self, documents: list[dict]) -> None:
        pass

    @abstractmethod
    async def search(
        self,
        query_embedding: list[float],
        limit: int = 10,
        filter_metadata: dict | None = None,
    ) -> list[SearchResult]:
        pass

    @abstractmethod
    async def delete(self, ids: list[str]) -> None:
        pass

    @abstractmethod
    async def get_collection_info(self) -> dict:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass
