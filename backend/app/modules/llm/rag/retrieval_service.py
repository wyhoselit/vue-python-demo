from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

from app.modules.llm.rag.retriever import retrieve

router = APIRouter()


class RetrievalRequest(BaseModel):
    query: str
    n_results: int = 5


@router.post("/retrieve")
async def retrieval_endpoint(request: RetrievalRequest):
    """
    API endpoint for retrieving relevant documents based on a query.
    """
    try:
        results = retrieve(request.query, request.n_results)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))