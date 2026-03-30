"""RAG engine -- ingestion, retrieval, and answer generation."""
from pathlib import Path

from backend.parsers.document_parser import parse_document
from backend.db.chroma_client import add_chunks, query_collection, get_collection_count

# Optional imports with graceful fallback
try:
    from sentence_transformers import SentenceTransformer

    _embedder = None

    def get_embedder():
        global _embedder
        if _embedder is None:
            _embedder = SentenceTransformer("all-MiniLM-L6-v2")
        return _embedder

except ImportError:

    def get_embedder():
        raise ImportError(
            "sentence-transformers required. "
            "Install with: pip install sentence-transformers"
        )


try:
    import anthropic

    _anthropic_client = None

    def get_anthropic_client():
        global _anthropic_client
        if _anthropic_client is None:
            _anthropic_client = anthropic.Anthropic()
        return _anthropic_client

except ImportError:

    def get_anthropic_client():
        raise ImportError(
            "anthropic SDK required. Install with: pip install anthropic"
        )


REGULATORY_DOCS_DIR = (
    Path(__file__).resolve().parent.parent / "data" / "regulatory_docs"
)


def ingest_documents() -> dict:
    """Ingest all PDFs from the regulatory_docs directory.

    Returns: {"documents_processed": int, "chunks_created": int,
              "status": str}
    """
    pdf_files = list(REGULATORY_DOCS_DIR.glob("*.pdf"))
    if not pdf_files:
        return {
            "documents_processed": 0,
            "chunks_created": 0,
            "status": "no_documents_found",
        }

    embedder = get_embedder()
    total_chunks = 0

    for pdf_path in pdf_files:
        chunks = parse_document(pdf_path)
        if chunks:
            texts = [c["text"] for c in chunks]
            embeddings = embedder.encode(texts).tolist()
            added = add_chunks(chunks, embeddings)
            total_chunks += added

    return {
        "documents_processed": len(pdf_files),
        "chunks_created": total_chunks,
        "status": "completed",
    }


def get_status() -> dict:
    """Get ingestion status.

    Returns: {"chunk_count": int, "status": str, "docs_dir": str}
    """
    count = get_collection_count()
    pdf_count = (
        len(list(REGULATORY_DOCS_DIR.glob("*.pdf")))
        if REGULATORY_DOCS_DIR.exists()
        else 0
    )
    return {
        "chunk_count": count,
        "document_count": pdf_count,
        "status": "ready" if count > 0 else "not_ingested",
        "docs_dir": str(REGULATORY_DOCS_DIR),
    }


def retrieve_context(question: str, n_results: int = 5) -> list[dict]:
    """Retrieve relevant chunks for a question.

    Returns: list of {"text": str, "document_name": str, "page": int,
             "section": str, "score": float}
    """
    embedder = get_embedder()
    query_embedding = embedder.encode(question).tolist()
    results = query_collection(query_embedding, n_results=n_results)

    context = []
    for doc, meta, dist in zip(
        results["documents"], results["metadatas"], results["distances"]
    ):
        context.append({
            "text": doc,
            "document_name": meta.get("document_name", ""),
            "page": meta.get("page", 0),
            "section": meta.get("section", ""),
            "score": 1 - dist,  # Convert distance to similarity
        })
    return context


def generate_answer(question: str, context_chunks: list[dict]) -> dict:
    """Generate answer from retrieved context using Claude.

    Returns: {"answer": str, "sources": list[dict], "model_used": str}
    """
    if not context_chunks:
        return {
            "answer": (
                "No relevant information was found in the regulatory "
                "document corpus for this question."
            ),
            "sources": [],
            "model_used": "none",
        }

    # Build context string
    context_text = ""
    for i, chunk in enumerate(context_chunks):
        context_text += f"\n\n---\nSource {i + 1}: {chunk['document_name']}"
        if chunk.get("section"):
            context_text += f" -- {chunk['section']}"
        context_text += f" (page {chunk['page']})\n{chunk['text']}"

    system_prompt = (
        "You are a regulatory guidance assistant for IVD diagnostic "
        "laboratories. Answer questions ONLY based on the provided document "
        "context. Always cite the source document name and section/page for "
        "each claim. If the answer is not supported by the provided context, "
        "explicitly state that the information was not found in the available "
        "documents. Do not speculate or provide information beyond what is in "
        "the context."
    )

    client = get_anthropic_client()
    response = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Context:{context_text}\n\nQuestion: {question}"
                ),
            }
        ],
    )

    answer_text = response.content[0].text

    sources = [
        {
            "document_name": c["document_name"],
            "section": c.get("section"),
            "page_number": c.get("page"),
            "chunk_preview": c["text"][:100],
        }
        for c in context_chunks
    ]

    return {
        "answer": answer_text,
        "sources": sources,
        "model_used": "claude-sonnet-4-6-20250514",
    }


def query(question: str) -> dict:
    """Full RAG pipeline: retrieve -> generate answer.

    Returns: {"answer": str, "sources": list, "model_used": str}
    """
    context = retrieve_context(question)
    return generate_answer(question, context)
