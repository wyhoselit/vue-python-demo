from unittest.mock import MagicMock, patch

import pytest

from app.modules.ai.services.chroma_vector_store import ChromaVectorStore
from app.modules.ai.services.vector_store import SearchResult


class TestChromaVectorStore:
    @pytest.fixture
    def mock_chroma_collection(self):
        collection = MagicMock()
        collection.query.return_value = {
            "ids": [["doc-1", "doc-2"]],
            "documents": [["Content 1", "Content 2"]],
            "metadatas": [[{"category": "test"}, {"category": "prod"}]],
            "distances": [[0.1, 0.3]],
        }
        collection.count.return_value = 2
        return collection

    @pytest.fixture
    def chroma_store(self, mock_chroma_collection):
        with patch("chromadb.PersistentClient") as mock_client:
            mock_client.return_value.get_or_create_collection.return_value = (
                mock_chroma_collection
            )
            store = ChromaVectorStore()
            store.collection = mock_chroma_collection
            return store

    @pytest.mark.asyncio
    async def test_add_documents(self, chroma_store):
        documents = [
            {
                "id": "1",
                "embedding": [0.1] * 384,
                "document": "Test doc",
                "metadata": {"key": "value"},
            }
        ]
        await chroma_store.add_documents(documents)
        chroma_store.collection.add.assert_called_once()

    @pytest.mark.asyncio
    async def test_search(self, chroma_store):
        results = await chroma_store.search([0.1] * 384, limit=2)
        assert len(results) == 2
        assert all(isinstance(r, SearchResult) for r in results)
        assert results[0].id == "doc-1"
        assert results[0].text == "Content 1"
        assert results[0].score == 0.9  # 1.0 - 0.1
        assert results[0].metadata == {"category": "test"}

    @pytest.mark.asyncio
    async def test_search_with_metadata_filter(self, chroma_store):
        await chroma_store.search(
            [0.1] * 384, limit=2, filter_metadata={"category": "test"}
        )
        chroma_store.collection.query.assert_called_once()
        call_kwargs = chroma_store.collection.query.call_args.kwargs
        assert call_kwargs["where"] == {"category": "test"}

    @pytest.mark.asyncio
    async def test_delete(self, chroma_store):
        await chroma_store.delete(["doc-1", "doc-2"])
        chroma_store.collection.delete.assert_called_once_with(ids=["doc-1", "doc-2"])

    @pytest.mark.asyncio
    async def test_health_check_success(self, chroma_store):
        assert await chroma_store.health_check() is True

    @pytest.mark.asyncio
    async def test_health_check_failure(self, chroma_store):
        chroma_store.collection.count.side_effect = Exception("Connection error")
        assert await chroma_store.health_check() is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
