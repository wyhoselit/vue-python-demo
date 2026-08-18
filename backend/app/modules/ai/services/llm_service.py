import asyncio
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass
class LLMCompletion:
    text: str
    model: str
    usage: dict[str, int]
    finish_reason: str = "stop"


RAG_PROMPT_TEMPLATE = """Use the following context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {query}

Answer:"""


class LLMProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMCompletion:
        pass

    @abstractmethod
    async def generate_stream(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        pass

    @abstractmethod
    async def get_models(self) -> list[str]:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None  # Initialize OpenAI client as needed
    
    async def generate(self, model: str, messages: list[dict[str, str]],
                      temperature: float = 0.7, max_tokens: int = 1000,
                      **kwargs) -> LLMCompletion:
        # Mock implementation for now
        return LLMCompletion(
            text="This is a mock response from OpenAI",
            model=model,
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            finish_reason="stop"
        )
    
    async def generate_stream(self, model: str, messages: list[dict[str, str]],
                              temperature: float = 0.7, max_tokens: int = 1000,
                              **kwargs) -> AsyncGenerator[str, None]:
        response = await self.generate(model, messages, temperature, max_tokens, **kwargs)
        # Simulate streaming
        words = response.text.split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.01)
    
    async def get_models(self) -> list[str]:
        return ["gpt-3.5-turbo", "gpt-4"]
    
    async def health_check(self) -> bool:
        return bool(self.api_key)


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def generate(self, model: str, messages: list[dict[str, str]],
                      temperature: float = 0.7, max_tokens: int = 1000,
                      **kwargs) -> LLMCompletion:
        # Mock implementation for now
        return LLMCompletion(
            text="This is a mock response from Anthropic",
            model=model,
            usage={"prompt_tokens": 15, "completion_tokens": 25, "total_tokens": 40},
            finish_reason="stop"
        )
    
    async def generate_stream(self, model: str, messages: list[dict[str, str]],
                              temperature: float = 0.7, max_tokens: int = 1000,
                              **kwargs) -> AsyncGenerator[str, None]:
        response = await self.generate(model, messages, temperature, max_tokens, **kwargs)
        words = response.text.split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.01)
    
    async def get_models(self) -> list[str]:
        return ["claude-3-opus", "claude-3-sonnet"]
    
    async def health_check(self) -> bool:
        return bool(self.api_key)


class LocalProvider(LLMProvider):
    def __init__(self):
        pass
    
    async def generate(self, model: str, messages: list[dict[str, str]],
                      temperature: float = 0.7, max_tokens: int = 1000,
                      **kwargs) -> LLMCompletion:
        # Mock implementation for now
        return LLMCompletion(
            text="This is a mock response from Local provider",
            model=model,
            usage={"prompt_tokens": 5, "completion_tokens": 10, "total_tokens": 15},
            finish_reason="stop"
        )
    
    async def generate_stream(self, model: str, messages: list[dict[str, str]],
                              temperature: float = 0.7, max_tokens: int = 1000,
                              **kwargs) -> AsyncGenerator[str, None]:
        response = await self.generate(model, messages, temperature, max_tokens, **kwargs)
        words = response.text.split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.01)
    
    async def get_models(self) -> list[str]:
        return ["llama2", "mistral"]
    
    async def health_check(self) -> bool:
        return True


class LLMService:
    def __init__(self):
        self.providers = {}
    
    def register_provider(self, name: str, provider: LLMProvider):
        self.providers[name] = provider
    
    async def get_provider(self, model: str) -> LLMProvider:
        for name, provider in self.providers.items():
            if model in await provider.get_models():
                return provider
        raise ValueError(f"No provider found for model: {model}")
    
    async def generate(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMCompletion:
        provider = await self.get_provider(model)
        return await provider.generate(model, messages, temperature, max_tokens, **kwargs)

    async def generate_with_rag(
        self,
        model: str,
        messages: list[dict[str, str]],
        query: str,
        context_documents: list[Document],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMCompletion:
        from app.modules.llm.rag.llm_integrator import (
            format_context_for_llm,
            generate_rag_prompt,
        )
        
        formatted_context = format_context_for_llm(context_documents)
        rag_prompt = generate_rag_prompt(query, formatted_context, RAG_PROMPT_TEMPLATE)
        
        # Replace the last user message with the RAG-augmented prompt
        rag_messages = messages[:-1] + [{"role": "user", "content": rag_prompt}]
        
        return await self.generate(model, rag_messages, temperature, max_tokens, **kwargs)

    
    async def generate_stream(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        provider = await self.get_provider(model)
        async for chunk in provider.generate_stream(model, messages, temperature, max_tokens, **kwargs):
            yield chunk

    async def stream_chat_with_rag(
        self,
        model: str,
        messages: list[dict[str, str]],
        query: str,
        context_documents: list[Document],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        from app.modules.llm.rag.llm_integrator import (
            format_context_for_llm,
            generate_rag_prompt,
        )

        formatted_context = format_context_for_llm(context_documents)
        rag_prompt = generate_rag_prompt(query, formatted_context, RAG_PROMPT_TEMPLATE)
        
        rag_messages = messages[:-1] + [{"role": "user", "content": rag_prompt}]

        async for chunk in self.generate_stream(model, rag_messages, temperature, max_tokens, **kwargs):
            yield chunk
    
    async def generate_chat(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        completion = await self.generate(model, messages, temperature, max_tokens, **kwargs)
        return completion.text
    
    async def stream_chat(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        async for chunk in self.generate_stream(model, messages, temperature, max_tokens, **kwargs):
            yield chunk