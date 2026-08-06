from app.modules.ai.services.llm_service import LLMService, OpenAIProvider, AnthropicProvider, LocalProvider
import os

def get_llm_service():
    service = LLMService()
    # In a real app, these keys would come from settings or env
    service.register_provider("openai", OpenAIProvider(api_key="mock-key"))
    service.register_provider("anthropic", AnthropicProvider(api_key="mock-key"))
    service.register_provider("local", LocalProvider())
    return service
