"""Regulatory RAG assistant endpoints."""
from fastapi import APIRouter, HTTPException

from backend.engine.rag_engine import ingest_documents, get_status, query
from backend.models.rag_schemas import (
    RAGStatusResponse,
    RAGIngestResponse,
    RAGQuery,
    RAGResponse,
    RAGSource,
)

router = APIRouter(prefix="/rag", tags=["rag"])


@router.get("/status", response_model=RAGStatusResponse)
def rag_status():
    """Get corpus ingestion status."""
    return get_status()


@router.post("/ingest", response_model=RAGIngestResponse)
def rag_ingest():
    """Trigger one-time ingestion of regulatory documents."""
    try:
        result = ingest_documents()
        return result
    except ImportError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/query", response_model=RAGResponse)
def rag_query(request: RAGQuery):
    """Query the regulatory assistant."""
    if not request.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty")
    try:
        result = query(request.question)
        return RAGResponse(
            answer=result["answer"],
            sources=[RAGSource(**s) for s in result["sources"]],
            model_used=result["model_used"],
        )
    except ImportError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Required dependency not available: {e}",
        )
