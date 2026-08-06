from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.api.v1.deps import get_current_user
from app.modules.user.user import User
from typing import AsyncGenerator
from pydantic import BaseModel
import json

router = APIRouter(tags=["ai"])

class ChatRequest(BaseModel):
    messages: list[dict]
    model: str
    temperature: float = 0.7
    max_tokens: int = 1000
    stream: bool = False

class EmbeddingRequest(BaseModel):
    text: str
    model: str

from app.modules.ai.api.deps import get_llm_service
from app.modules.ai.services.llm_service import LLMService

@router.post("/chat")
async def chat_completion(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    service: LLMService = Depends(get_llm_service)
):
    if request.stream:
        async def generate():
            async for chunk in service.stream_chat(request.messages, request.model):
                yield chunk
        return StreamingResponse(generate(), media_type="text/plain")
    
    completion = await service.generate(request.model, request.messages, request.temperature, request.max_tokens)
    return {
        "text": completion.text,
        "model": completion.model,
        "usage": completion.usage
    }

@router.post("/embeddings")
async def embeddings(
    request: EmbeddingRequest,
    current_user: User = Depends(get_current_user),
    service: LLMService = Depends(get_llm_service)
):
    from ..services.vector_service import VectorService
    # VectorService might need to be initialized similarly
    # Assuming VectorService is stateless for now or doesn't need service registration
    vector_service = VectorService()
    embedding = await vector_service.generate_embedding(
        text=request.text,
        model=request.model
    )
    return {"embedding": embedding, "model": request.model}
