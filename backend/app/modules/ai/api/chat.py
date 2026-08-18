from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.api.v1.deps import get_current_user
from app.modules.user.user import User
from typing import AsyncGenerator, List
from pydantic import BaseModel

from app.modules.llm.rag.retriever import retrieve
from langchain_core.documents import Document

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

class RAGQueryRequest(BaseModel):
    query: str
    model: str
    n_results: int = 5
    temperature: float = 0.7
    max_tokens: int = 1000
    stream: bool = False

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

@router.post("/rag_chat")
async def rag_chat_completion(
    request: RAGQueryRequest,
    current_user: User = Depends(get_current_user),
    service: LLMService = Depends(get_llm_service)
):
    # 1. Retrieve relevant documents
    retrieval_results = await retrieve(request.query, request.n_results)
    
    # Format documents for LLM context (assuming retrieval_results['documents'] contains the text)
    context_documents = []
    for doc_content, metadata in zip(retrieval_results['documents'][0], retrieval_results['metadatas'][0]):
        context_documents.append(Document(page_content=doc_content, metadata=metadata))

    # 2. Generate LLM response with RAG context
    messages = [{"role": "user", "content": request.query}] # Only the query, context handled by RAG
    
    if request.stream:
        async def generate_rag_stream():
            async for chunk in service.stream_chat_with_rag(
                model=request.model,
                messages=messages,
                query=request.query,
                context_documents=context_documents,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ):
                yield chunk
        return StreamingResponse(generate_rag_stream(), media_type="text/plain")
    
    completion = await service.generate_with_rag(
        model=request.model,
        messages=messages,
        query=request.query,
        context_documents=context_documents,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    return {
        "text": completion.text,
        "model": completion.model,
        "usage": completion.usage,
        "retrieved_docs": retrieval_results # Optionally return retrieved docs for debugging
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
