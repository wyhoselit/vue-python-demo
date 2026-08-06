from typing import List, Optional
from dataclasses import dataclass


@dataclass
class SearchResult:
    id: str
    text: str
    score: float
    metadata: dict


class VectorService:
    async def generate_embedding(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        return [0.0] * 1536  # ponytail: stub; replace with real provider call when OpenAI dep wired

    async def store_embedding(self, id: str, text: str, embedding: List[float], metadata: Optional[dict] = None):
        pass  # ponytail: stub; needs pgvector table + SQLAlchemy insert

    async def search(self, query_embedding: List[float], limit: int = 10) -> List[SearchResult]:
        return []  # ponytail: stub; needs pgvector cosine similarity query