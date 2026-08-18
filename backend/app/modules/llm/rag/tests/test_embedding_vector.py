import pytest
from unittest.mock import MagicMock, patch, Mock
import chromadb
from chromadb.config import Settings

from app.modules.llm.rag.embedding_generator import EmbeddingGenerator
from app.modules.llm.rag.vector_store import VectorStore, get_vector_store

# --- Test Embedding Generator ---

@pytest.fixture
def mock_embedding_generator_sentence_transformer():
    with patch('app.modules.llm.rag.embedding_generator.SentenceTransformer') as mock_st:
        mock_instance = MagicMock()
        mock_instance.encode.return_value = MagicMock(tolist=lambda: [0.1, 0.2, 0.3])
        mock_st.return_value = mock_instance
        yield mock_st

def test_embedding_generator_init(mock_embedding_generator_sentence_transformer):
    # The actual model is created inside the class, so we check if the mock was called
    EmbeddingGenerator(model_name='test-model')
    mock_embedding_generator_sentence_transformer.assert_called_once_with('test-model')

def test_generate_single_embedding(mock_embedding_generator_sentence_transformer):
    mock_instance = mock_embedding_generator_sentence_transformer.return_value
    mock_instance.encode.return_value = MagicMock(tolist=lambda: [0.1, 0.2, 0.3])
    
    generator = EmbeddingGenerator(model_name='test-model')
    embedding = generator.generate_embedding("test text")
    
    assert embedding == [0.1, 0.2, 0.3]
    mock_instance.encode.assert_called_once_with("test text")

def test_generate_multiple_embeddings(mock_embedding_generator_sentence_transformer):
    mock_instance = mock_embedding_generator_sentence_transformer.return_value
    mock_instance.encode.return_value = MagicMock(tolist=lambda: [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
    
    generator = EmbeddingGenerator(model_name='test-model')
    embeddings = generator.generate_embeddings(["text1", "text2"])
    
    assert len(embeddings) == 2
    assert embeddings[0] == [0.1, 0.2, 0.3]
    assert embeddings[1] == [0.4, 0.5, 0.6]
    mock_instance.encode.assert_called_once_with(["text1", "text2"])

# --- Test Vector Store ---

@pytest.fixture
def mock_chromadb_client():
    with patch('app.modules.llm.rag.vector_store.chromadb.PersistentClient') as mock_client:
        mock_collection = MagicMock()
        mock_collection.count.return_value = 10
        mock_collection.name = "rag_documents"
        mock_client.return_value.get_or_create_collection.return_value = mock_collection
        yield mock_client, mock_collection

def test_vector_store_init(mock_chromadb_client):
    mock_client, mock_collection = mock_chromadb_client
    
    store = VectorStore(persist_directory="./test_db", collection_name="test_collection")
    
    assert store.collection.name == mock_collection.name
    mock_client.assert_called_once_with(
        path="./test_db",
        settings=Settings(anonymized_telemetry=False)
    )
    mock_client.return_value.get_or_create_collection.assert_called_once_with(name="test_collection")

def test_vector_store_add_documents(mock_chromadb_client):
    mock_client, mock_collection = mock_chromadb_client
    
    store = VectorStore()
    docs = [
        {'id': '1', 'embedding': [0.1, 0.2], 'document': 'doc1', 'metadata': {'source': 'test'}},
        {'id': '2', 'embedding': [0.3, 0.4], 'document': 'doc2', 'metadata': {'source': 'test'}}
    ]
    
    store.add_documents(docs)
    
    mock_collection.add.assert_called_once_with(
        ids=['1', '2'],
        embeddings=[[0.1, 0.2], [0.3, 0.4]],
        documents=['doc1', 'doc2'],
        metadatas=[{'source': 'test'}, {'source': 'test'}]
    )

def test_vector_store_query(mock_chromadb_client):
    mock_client, mock_collection = mock_chromadb_client
    mock_collection.query.return_value = {
        'ids': [['1', '2']],
        'documents': [['doc1', 'doc2']],
        'metadatas': [[{'source': 'test'}, {'source': 'test'}]],
        'distances': [[0.1, 0.2]]
    }
    
    store = VectorStore()
    result = store.query([0.1, 0.2], n_results=2)
    
    assert result == {
        'ids': [['1', '2']],
        'documents': [['doc1', 'doc2']],
        'metadatas': [[{'source': 'test'}, {'source': 'test'}]],
        'distances': [[0.1, 0.2]]
    }
    mock_collection.query.assert_called_once_with(
        query_embeddings=[[0.1, 0.2]],
        n_results=2
    )

def test_vector_store_get_collection_info(mock_chromadb_client):
    mock_client, mock_collection = mock_chromadb_client
    
    store = VectorStore()
    info = store.get_collection_info()
    
    assert info == {"name": "rag_documents", "count": 10}

def test_get_vector_store_singleton():
    # Reset global singleton
    import app.modules.llm.rag.vector_store as vs_module
    vs_module._vector_store = None
    
    with patch('chromadb.PersistentClient') as mock_client:
        mock_collection = MagicMock()
        mock_client.return_value.get_or_create_collection.return_value = mock_collection
        
        store1 = get_vector_store()
        store2 = get_vector_store()
        
        assert store1 is store2
        assert mock_client.call_count == 1