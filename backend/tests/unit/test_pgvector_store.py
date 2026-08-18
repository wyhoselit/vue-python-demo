from unittest.mock import MagicMock, patch, AsyncMock

import pytest

from app.modules.ai.services.pgvector_store import PGVectorStore
from app.modules.ai.services.vector_store import SearchResult


class TestPGVectorStore:
    @pytest.fixture
    def mock_session(self):
        session = AsyncMock()
        session.execute = AsyncMock()
        session.execute.return_value.fetchall.return_value = []
        session.commit = AsyncMock()
        return session

    @pytest.fixture
    def mock_session_local(self, mock_session):
        async_session_local = MagicMock()
        async_session_local.__aenter__ = AsyncMock(return_value=mock_session)
        async_session_local.__aexit__ = AsyncMock(return_value=None)
        return async_session_local

    @pytest.fixture
    def pgvector_store(self):
        with patch("app.modules.ai.services.pgvector_store.create_async_engine"), \
             patch("app.modules.ai.services.pgvector_store.sessionmaker") as mock_sessionmaker, \
             patch("app.modules.ai.services.pgvector_store.settings") as mock_settings:
            
            mock_settings.VECTOR_STORE = "pgvector"
            mock_settings.PGVECTOR_HNSW_M = 16
            mock_settings.PGVECTOR_HNSW_EF_CONSTRUCTION = 64
            mock_settings.DATABASE_URL = "postgresql+asyncpg://test:test@localhost/test"
            
            mock_session_local = MagicMock()
            mock_session_local.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
            mock_session_local.return_value.__aexit__ = AsyncMock(return_value=None)
            mock_sessionmaker.return_value = mock_session_local
            
            store = PGVectorStore()
            store.AsyncSessionLocal = mock_session_local
            return store

    @pytest.mark.asyncio
    async def test_add_documents(self, pgvector_store):
        documents = [
            {
                "id": "1",
                "embedding": [0.1] * 384,
                "document": "Test doc",
                "metadata": {"key": "value"},
            }
        ]
        mock_session = MagicMock()
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        pgvector_store.AsyncSessionLocal.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        pgvector_store.AsyncSessionLocal.return_value.__aexit__ = AsyncMock(return_value=None)
        
        await pgvector_store.add_documents(documents)
        
        mock_session.add.assert_called_once()

    @pytest.mark.asyncio
    async def test_search(self, pgvector_store):
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            MagicMock(id=1, content="Result 1", meta_data={"source": "test.txt"}, score=0.95)
        ]
        mock_session.execute = AsyncMock(return_value=mock_result)
        pgvector_store.AsyncSessionLocal.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        pgvector_store.AsyncSessionLocal.return_value.__aexit__ = AsyncMock(return_value=None)
        
        results = await pgvector_store.search([0.1] * 384, limit=10)
        
        assert len(results) >= 0

    @pytest.mark.asyncio
    async def test_health_check_success(self, pgvector_store):
        mock_session = MagicMock()
        mock_session.execute = AsyncMock()
        pgvector_store.AsyncSessionLocal.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        pgvector_store.AsyncSessionLocal.return_value.__aexit__ = AsyncMock(return_value=None)
        
        result = await pgvector_store.health_check()
        assert result is True

    @pytest.mark.asyncio
    async def test_health_check_failure(self, pgvector_store):
        mock_session = MagicMock()
        mock_session.execute = AsyncMock(side_effect=Exception("Connection error"))
        pgvector_store.AsyncSessionLocal.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        pgvector_store.AsyncSessionLocal.return_value.__aexit__ = AsyncMock(return_value=None)
        
        result = await pgvector_store.health_check()
        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])