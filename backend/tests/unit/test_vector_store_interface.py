import pytest

from app.modules.ai.services.vector_store import SearchResult, VectorStore


class MockVectorStore(VectorStore):
    async def add_documents(self, documents: list[dict]) -> None:
        pass

    async def search(
        self,
        query_embedding: list[float],
        limit: int = 10,
        filter_metadata=None,
    ) -> list[SearchResult]:
        return []

    async def delete(self, ids: list[str]) -> None:
        pass

    async def get_collection_info(self) -> dict:
        return {"name": "mock", "count": 0}

    async def health_check(self) -> bool:
        return True


def test_search_result_dataclass():
    result = SearchResult(
        id="doc-1",
        text="Test content",
        score=0.95,
        metadata={"category": "test", "source": "manual"},
    )
    assert result.id == "doc-1"
    assert result.text == "Test content"
    assert result.score == 0.95
    assert result.metadata == {"category": "test", "source": "manual"}


@pytest.mark.asyncio
async def test_vector_store_interface_contract():
    store = MockVectorStore()

    await store.add_documents([{"id": "1", "text": "doc1", "metadata": {}}])

    results = await store.search([0.1, 0.2, 0.3], limit=5)
    assert isinstance(results, list)

    await store.delete(["1"])

    is_healthy = await store.health_check()
    assert is_healthy is True
