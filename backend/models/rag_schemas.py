"""Pydantic schemas for RAG assistant API."""
from pydantic import BaseModel


class RAGStatusResponse(BaseModel):
    chunk_count: int
    document_count: int
    status: str  # "ready"|"not_ingested"
    docs_dir: str


class RAGIngestResponse(BaseModel):
    documents_processed: int
    chunks_created: int
    status: str


class RAGQuery(BaseModel):
    question: str


class RAGSource(BaseModel):
    document_name: str
    section: str | None = None
    page_number: int | None = None
    chunk_preview: str


class RAGResponse(BaseModel):
    answer: str
    sources: list[RAGSource]
    model_used: str
