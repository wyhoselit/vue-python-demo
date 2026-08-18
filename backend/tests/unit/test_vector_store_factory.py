from unittest.mock import MagicMock, patch

import pytest

from app.modules.ai.services.vector_store import VectorStore
from app.modules.ai.services.vector_store_factory import (
    get_vector_store,
    reset_vector_store,
)


class TestVectorStoreFactory:
    def setup_method(self):
        reset_vector_store()

    def test_get_vector_store_returns_chroma_by_default(self):
        mock_chroma = MagicMock(spec=VectorStore)
        with (
            patch(
                "app.modules.ai.services.vector_store_factory.settings"
            ) as mock_settings,
            patch(
                "app.modules.ai.services.chroma_vector_store.ChromaVectorStore",
                return_value=mock_chroma,
            ),
        ):
            mock_settings.VECTOR_STORE = "chroma"
            store = get_vector_store()
            assert store is mock_chroma

    def test_get_vector_store_returns_chroma_when_specified(self):
        mock_chroma = MagicMock(spec=VectorStore)
        with (
            patch(
                "app.modules.ai.services.vector_store_factory.settings"
            ) as mock_settings,
            patch(
                "app.modules.ai.services.chroma_vector_store.ChromaVectorStore",
                return_value=mock_chroma,
            ),
        ):
            mock_settings.VECTOR_STORE = "chroma"
            store = get_vector_store()
            assert store is mock_chroma

    def test_get_vector_store_returns_pgvector_when_specified(self):
        mock_pgvector = MagicMock(spec=VectorStore)
        with (
            patch(
                "app.modules.ai.services.vector_store_factory.settings"
            ) as mock_settings,
            patch(
                "app.modules.ai.services.pgvector_store.PGVectorStore",
                return_value=mock_pgvector,
            ),
        ):
            mock_settings.VECTOR_STORE = "pgvector"
            store = get_vector_store()
            assert store is mock_pgvector

    def test_get_vector_store_raises_for_unknown_value(self):
        with patch(
            "app.modules.ai.services.vector_store_factory.settings"
        ) as mock_settings:
            mock_settings.VECTOR_STORE = "unknown"
            with pytest.raises(ValueError, match="Unknown VECTOR_STORE: unknown"):
                get_vector_store()

    def test_get_vector_store_returns_same_instance(self):
        mock_chroma = MagicMock(spec=VectorStore)
        with (
            patch(
                "app.modules.ai.services.vector_store_factory.settings"
            ) as mock_settings,
            patch(
                "app.modules.ai.services.chroma_vector_store.ChromaVectorStore",
                return_value=mock_chroma,
            ),
        ):
            mock_settings.VECTOR_STORE = "chroma"
            store1 = get_vector_store()
            store2 = get_vector_store()
            assert store1 is store2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
