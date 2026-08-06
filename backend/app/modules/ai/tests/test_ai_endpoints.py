import pytest
from starlette.testclient import TestClient
from app.modules.ai.services.llm_service import LLMService, OpenAIProvider

def test_ai_chat_endpoint_unauthorized(client: TestClient):
    response = client.post("/api/v1/ai/chat", json={
        "messages": [{"role": "user", "content": "hello"}],
        "model": "gpt-3.5-turbo"
    })
    assert response.status_code == 401

def test_ai_chat_endpoint_authorized(client: TestClient):
    # Register and login
    client.post("/api/v1/auth/register", json={"email": "test@example.com", "password": "password123"})
    login_response = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "password123"})
    access_token = login_response.cookies.get("access_token")
    client.cookies.set("access_token", access_token)
    
    response = client.post("/api/v1/ai/chat", json={
        "messages": [{"role": "user", "content": "hello"}],
        "model": "gpt-3.5-turbo"
    })
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "model" in data
    assert "usage" in data

def test_ai_chat_endpoint_streaming(client: TestClient):
    client.post("/api/v1/auth/register", json={"email": "test2@example.com", "password": "password123"})
    login_response = client.post("/api/v1/auth/login", json={"email": "test2@example.com", "password": "password123"})
    access_token = login_response.cookies.get("access_token")
    client.cookies.set("access_token", access_token)
    
    response = client.post("/api/v1/ai/chat", json={
        "messages": [{"role": "user", "content": "hello"}],
        "model": "gpt-3.5-turbo",
        "stream": True
    })
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"

def test_ai_embeddings_endpoint(client: TestClient):
    client.post("/api/v1/auth/register", json={"email": "test3@example.com", "password": "password123"})
    login_response = client.post("/api/v1/auth/login", json={"email": "test3@example.com", "password": "password123"})
    access_token = login_response.cookies.get("access_token")
    client.cookies.set("access_token", access_token)
    
    response = client.post("/api/v1/ai/embeddings", json={
        "text": "test text",
        "model": "text-embedding-ada-002"
    })
    assert response.status_code == 200
    data = response.json()
    assert "embedding" in data
    assert "model" in data
    assert isinstance(data["embedding"], list)

def test_llm_service_providers():
    service = LLMService()
    provider = OpenAIProvider(api_key="test-key")
    service.register_provider("openai", provider)
    
    assert "openai" in service.providers
    assert service.providers["openai"] == provider

@pytest.mark.asyncio
async def test_llm_service_generate():
    service = LLMService()
    provider = OpenAIProvider(api_key="test-key")
    service.register_provider("openai", provider)
    
    result = await service.generate("gpt-3.5-turbo", [{"role": "user", "content": "hello"}])
    assert result.model == "gpt-3.5-turbo"
    assert "mock" in result.text
    assert result.usage.get("prompt_tokens") == 10