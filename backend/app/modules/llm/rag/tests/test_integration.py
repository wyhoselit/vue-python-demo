import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from langchain_core.documents import Document

from app.modules.llm.rag.retriever import retrieve, generate_query_embedding
from app.modules.ai.services.llm_service import LLMService, LLMCompletion
from app.modules.ai.api.chat import rag_chat_completion


# --- Integration Test: Retrieval + LLM Generation ---

@pytest.mark.asyncio
async def test_rag_chat_completion_integration():
    """
    Integration test for RAG chat completion endpoint.
    Mocks both retrieval and LLM service.
    """
    # Mock the retrieval
    mock_retrieval_results = {
        'ids': [['doc1', 'doc2']],
        'documents': [['Context document 1 about Python', 'Context document 2 about FastAPI']],
        'metadatas': [[{'source': 'python.txt'}, {'source': 'fastapi.txt'}]],
        'distances': [[0.1, 0.2]]
    }
    
    # Mock LLM service
    mock_llm_service = MagicMock()
    mock_llm_service.generate_with_rag = AsyncMock(return_value=LLMCompletion(
        text="Based on the context, Python is a programming language.",
        model="gpt-3.5-turbo",
        usage={"prompt_tokens": 50, "completion_tokens": 10, "total_tokens": 60},
        finish_reason="stop"
    ))
    
    # Mock the user
    mock_user = MagicMock()
    mock_user.id = "test_user"
    
    # Call the endpoint
    request = MagicMock()
    request.query = "What is Python?"
    request.model = "gpt-3.5-turbo"
    request.n_results = 5
    request.temperature = 0.7
    request.max_tokens = 1000
    request.stream = False
    
    with patch('app.modules.ai.api.chat.retrieve', new_callable=AsyncMock) as mock_retrieve:
        mock_retrieve.return_value = mock_retrieval_results
        response = await rag_chat_completion(request, mock_user, mock_llm_service)
    
    assert response["text"] == "Based on the context, Python is a programming language."
    assert response["model"] == "gpt-3.5-turbo"
    assert response["usage"]["total_tokens"] == 60
    assert "retrieved_docs" in response


@pytest.mark.asyncio
async def test_rag_chat_completion_streaming():
    """
    Integration test for streaming RAG chat completion.
    """
    mock_retrieval_results = {
        'ids': [['doc1']],
        'documents': [['Test document']],
        'metadatas': [[{'source': 'test.txt'}]],
        'distances': [[0.1]]
    }
    
    mock_llm_service = MagicMock()
    async def mock_stream(*args, **kwargs):
        yield "Test "
        yield "stream "
        yield "response"
    
    mock_llm_service.stream_chat_with_rag = mock_stream
    
    mock_user = MagicMock()
    request = MagicMock()
    request.query = "Test query"
    request.model = "gpt-3.5-turbo"
    request.n_results = 5
    request.temperature = 0.7
    request.max_tokens = 1000
    request.stream = True
    
    with patch('app.modules.ai.api.chat.retrieve', new_callable=AsyncMock) as mock_retrieve:
        mock_retrieve.return_value = mock_retrieval_results
        response = await rag_chat_completion(request, mock_user, mock_llm_service)
    
    assert hasattr(response, 'media_type')
    assert response.media_type == "text/plain"


# --- Integration Test: LLMService with RAG ---

@pytest.mark.asyncio
async def test_llm_service_generate_with_rag():
    """
    Test LLMService generate_with_rag method with mocked provider.
    """
    from app.modules.ai.services.llm_service import LLMProvider
    
    mock_provider = MagicMock(spec=LLMProvider)
    mock_provider.get_models = AsyncMock(return_value=["test-model"])
    mock_provider.generate = AsyncMock(return_value=LLMCompletion(
        text="RAG response",
        model="test-model",
        usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        finish_reason="stop"
    ))
    
    service = LLMService()
    service.register_provider("test", mock_provider)
    
    context_docs = [
        Document(page_content="Context 1", metadata={"source": "test1.txt"}),
        Document(page_content="Context 2", metadata={"source": "test2.txt"})
    ]
    
    messages = [{"role": "user", "content": "What is X?"}]
    
    completion = await service.generate_with_rag(
        model="test-model",
        messages=messages,
        query="What is X?",
        context_documents=context_docs
    )
    
    assert completion.text == "RAG response"
    mock_provider.generate.assert_called_once()
    
    # Verify the RAG prompt was constructed
    call_args = mock_provider.generate.call_args
    assert "Context 1" in call_args[0][1][-1]["content"]  # Check RAG prompt includes context
    assert "Context 2" in call_args[0][1][-1]["content"]
    assert "What is X?" in call_args[0][1][-1]["content"]


@pytest.mark.asyncio
async def test_llm_service_stream_chat_with_rag():
    """
    Test LLMService stream_chat_with_rag method.
    """
    from app.modules.ai.services.llm_service import LLMProvider
    
    mock_provider = MagicMock(spec=LLMProvider)
    mock_provider.get_models = AsyncMock(return_value=["test-model"])
    
    async def mock_stream(*args, **kwargs):
        yield "Streaming "
        yield "RAG "
        yield "response"
    
    mock_provider.generate_stream = mock_stream
    
    service = LLMService()
    service.register_provider("test", mock_provider)
    
    context_docs = [Document(page_content="Context", metadata={"source": "test.txt"})]
    messages = [{"role": "user", "content": "Query?"}]
    
    chunks = []
    async for chunk in service.stream_chat_with_rag(
        model="test-model",
        messages=messages,
        query="Query?",
        context_documents=context_docs
    ):
        chunks.append(chunk)
    
    assert chunks == ["Streaming ", "RAG ", "response"]


# --- Integration Test: Retrieval ---

@pytest.mark.asyncio
async def test_retrieve_integration():
    """
    Integration test for retrieve function with mocked vector store.
    """
    with patch('app.modules.llm.rag.retriever.generate_query_embedding') as mock_embed, \
         patch('app.modules.llm.rag.retriever.get_vector_store') as mock_get_store:
        
        mock_embed.return_value = [0.1, 0.2, 0.3]
        mock_store = MagicMock()
        mock_store.search = AsyncMock(return_value=[
            MagicMock(
                id="doc1",
                text="Retrieved document",
                metadata={"source": "test.txt"},
                score=0.95
            )
        ])
        mock_get_store.return_value = mock_store
        
        results = await retrieve("test query", n_results=3)
        
        assert results['documents'][0] == ['Retrieved document']
        mock_embed.assert_called_once_with("test query")
        mock_store.search.assert_called_once_with([0.1, 0.2, 0.3], 3, None)


# --- Integration Test: End-to-End Ingestion and Retrieval ---

@pytest.mark.asyncio
async def test_ingest_and_retrieve_flow():
    """
    Test the full ingestion -> vector store -> retrieval flow with mocks.
    """
    from app.modules.llm.rag.ingestion_service import ingest_and_store_document
    from app.modules.ai.services.chroma_vector_store import ChromaVectorStore
    from app.modules.ai.services.vector_store_factory import reset_vector_store
    
    reset_vector_store()

    # Mock document loading
    mock_docs = [Document(page_content="Test document content", metadata={"source": "test.txt"})]
    
    with patch('app.modules.llm.rag.ingestion_service.load_document', return_value=mock_docs), \
         patch('app.modules.llm.rag.ingestion_service.split_documents', return_value=mock_docs), \
         patch('app.modules.llm.rag.embedding_generator.EmbeddingGenerator.generate_embeddings', return_value=[[0.1, 0.2, 0.3]]), \
         patch('app.modules.ai.services.chroma_vector_store.ChromaVectorStore') as mock_chroma_class:
    
        mock_collection = MagicMock()
        mock_chroma_instance = MagicMock()
        mock_chroma_instance.collection = mock_collection
        mock_chroma_class.return_value = mock_chroma_instance
        
        # Test ingestion
        chunks = await ingest_and_store_document("test.txt")
        
        assert len(chunks) == 1
        assert chunks[0].page_content == "Test document content"
        assert 'embedding' in chunks[0].metadata
        
        # Verify vector store add was called
        mock_chroma_instance.add_documents.assert_called_once()
        added_docs_call_args = mock_chroma_instance.add_documents.call_args[0][0]
        
        assert added_docs_call_args[0]['id'] == 'test.txt_0'
        assert added_docs_call_args[0]['embedding'] == [0.1, 0.2, 0.3]
        assert added_docs_call_args[0]['document'] == 'Test document content'
        assert added_docs_call_args[0]['metadata']['source'] == 'test.txt'
        assert 'embedding' not in added_docs_call_args[0]['metadata']