import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from app.modules.ai.services.llm_service import LLMService, OpenAIProvider

@pytest.mark.asyncio
async def test_llm_service_openai():
    service = LLMService()
    provider = OpenAIProvider(api_key="test-key")
    service.register_provider("openai", provider)
    
    result = await service.generate("gpt-3.5-turbo", [{"role": "user", "content": "hello"}])
    assert result.model == "gpt-3.5-turbo"
    assert "mock" in result.text
