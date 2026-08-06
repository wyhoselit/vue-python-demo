""""Dramatiq actors for AI tasks (embedding generation and batch inference)"""

from dramatiq import actor
from typing import Dict, Any
from backend.app.modules.ai.services.llm_service import LLMService
from backend.app.modules.ai.services.vector_service import VectorService


@actor
def generate_embedding(text: str, model: str = "text-embedding-ada-002") -> Dict[str, Any]:
    """Generate embedding for a single text"""
    service = VectorService()
    embedding = await service.generate_embedding(text, model)
    return {"text": text, "embedding": embedding, "model": model, "status": "success"}


@actor
def generate_batch_embeddings(texts: list[str], model: str = "text-embedding-ada-002") -> Dict[str, Any]:
    """Generate embeddings for multiple texts in batch"""
    service = VectorService()
    embeddings = []
    for text in texts:
        embedding = await service.generate_embedding(text, model)
        embeddings.append(embedding)
    
    return {
        "texts": texts,
        "embeddings": embeddings,
        "model": model,
        "count": len(embeddings),
        "status": "success"
    }


@actor
def generate_llm_completion(
    model: str,
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> Dict[str, Any]:
    """Generate LLM completion"""
    service = LLMService()
    result = await service.generate(model, messages, temperature, max_tokens)
    return {
        "text": result.text,
        "model": result.model,
        "usage": result.usage,
        "finish_reason": result.finish_reason,
        "status": "success"
    }


@actor
def generate_batch_llm_completions(
    tasks: list[tuple],
    model: str = "gpt-3.5-turbo"
) -> Dict[str, Any]:
    """Generate LLM completions for multiple tasks"""
    service = LLMService()
    results = []
    
    for task in tasks:
        completion = await service.generate(model, task["messages"], task.get("temperature", 0.7), task.get("max_tokens", 1000))
        results.append({
            "text": completion.text,
            "model": completion.model,
            "usage": completion.usage,
            "finish_reason": completion.finish_reason,
            "task_id": task.get("id", str(len(results)))
        })
    
    return {
        "results": results,
        "model": model,
        "count": len(results),
        "status": "success"
    }


@actor
def health_check_all() -> Dict[str, Any]:
    """Check health of all AI services"""
    llm_service = LLMService()
    vector_service = VectorService()
    
    llm_health = await llm_service.health_check()
    vector_health = await vector_service.health_check() if hasattr(vector_service, "health_check") else True
    
    return {
        "llm_service": llm_health,
        "vector_service": vector_health,
        "status": "ok" if (llm_health and vector_health) else "degraded"
    }