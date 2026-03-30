"""ChromaDB client for regulatory document embeddings."""
from pathlib import Path

try:
    import chromadb
except ImportError:
    chromadb = None

_PERSIST_DIR = Path(__file__).resolve().parent.parent / "data" / "chroma_db"
_COLLECTION_NAME = "regulatory_docs_v1"

_client = None
_collection = None


def get_client():
    """Get or create the ChromaDB client."""
    global _client
    if chromadb is None:
        raise ImportError(
            "chromadb is required. Install with: pip install chromadb"
        )
    if _client is None:
        _PERSIST_DIR.mkdir(parents=True, exist_ok=True)
        _client = chromadb.PersistentClient(path=str(_PERSIST_DIR))
    return _client


def get_collection():
    """Get or create the regulatory docs collection."""
    global _collection
    if _collection is None:
        client = get_client()
        _collection = client.get_or_create_collection(
            name=_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def add_chunks(chunks: list[dict], embeddings: list[list[float]]) -> int:
    """Add document chunks with pre-computed embeddings to the collection.

    Returns number of chunks added.
    """
    collection = get_collection()
    ids = [
        f"{c['document_name']}_p{c['page']}_c{c['chunk_index']}"
        for c in chunks
    ]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {
            "document_name": c["document_name"],
            "page": c["page"],
            "chunk_index": c["chunk_index"],
            "section": c.get("section") or "",
        }
        for c in chunks
    ]
    collection.add(
        ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas
    )
    return len(ids)


def query_collection(
    query_embedding: list[float], n_results: int = 5
) -> dict:
    """Query the collection with an embedding vector.

    Returns: {"documents": list[str], "metadatas": list[dict],
              "distances": list[float]}
    """
    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_embedding], n_results=n_results
    )
    return {
        "documents": results["documents"][0] if results["documents"] else [],
        "metadatas": results["metadatas"][0] if results["metadatas"] else [],
        "distances": results["distances"][0] if results["distances"] else [],
    }


def get_collection_count() -> int:
    """Return number of chunks in the collection."""
    try:
        return get_collection().count()
    except Exception:
        return 0
