"""Tests for the Regulatory RAG module.

Covers document_parser chunking logic (no ML deps required)
and ChromaDB client (skipped if chromadb is not installed).
"""
import pytest

from backend.parsers.document_parser import chunk_text


# ---------------------------------------------------------------------------
# chunk_text tests -- pure Python, no optional dependencies
# ---------------------------------------------------------------------------

class TestChunkText:
    """Tests for clause-boundary-aware text chunking."""

    def _make_pages(self, texts: list[str]) -> list[dict]:
        """Helper: wrap raw text strings into page dicts."""
        return [{"page": i + 1, "text": t} for i, t in enumerate(texts)]

    def test_basic_chunking_produces_chunks(self):
        """A page with enough words should produce at least one chunk."""
        text = " ".join(["word"] * 500)
        pages = self._make_pages([text])
        chunks = chunk_text(pages, chunk_size=512, overlap=64, document_name="test_doc")
        assert len(chunks) >= 1

    def test_chunk_metadata_fields(self):
        """Each chunk must carry document_name, page, chunk_index, section."""
        text = " ".join(["hello"] * 100)
        pages = self._make_pages([text])
        chunks = chunk_text(pages, chunk_size=512, overlap=64, document_name="my_doc")
        for chunk in chunks:
            assert "text" in chunk
            assert chunk["document_name"] == "my_doc"
            assert chunk["page"] == 1
            assert "chunk_index" in chunk
            assert "section" in chunk

    def test_chunk_index_sequential(self):
        """chunk_index values should be sequential starting from 0."""
        text = " ".join(["token"] * 1000)
        pages = self._make_pages([text])
        chunks = chunk_text(pages, chunk_size=128, overlap=16, document_name="seq")
        indices = [c["chunk_index"] for c in chunks]
        assert indices == list(range(len(indices)))

    def test_empty_pages_return_no_chunks(self):
        """An empty page list should produce no chunks."""
        chunks = chunk_text([], chunk_size=512, overlap=64, document_name="empty")
        assert chunks == []

    def test_page_with_only_whitespace_produces_no_chunks(self):
        """A page whose text is only whitespace has no words to chunk.

        Note: extract_text_pymupdf filters these out, but chunk_text should
        handle them gracefully too (produces empty-text chunk or skips).
        """
        pages = [{"page": 1, "text": "   \n\n  "}]
        chunks = chunk_text(pages, chunk_size=512, overlap=64, document_name="ws")
        # Either no chunks or chunks with empty/whitespace text
        assert len(chunks) == 0

    def test_document_name_preserved(self):
        """document_name should appear in every chunk."""
        pages = self._make_pages(["Some regulatory text here"])
        chunks = chunk_text(pages, document_name="CDSCO_MD15")
        assert all(c["document_name"] == "CDSCO_MD15" for c in chunks)

    def test_page_numbers_preserved(self):
        """Chunks from page 2 should have page=2."""
        pages = [
            {"page": 1, "text": " ".join(["alpha"] * 50)},
            {"page": 2, "text": " ".join(["beta"] * 50)},
        ]
        chunks = chunk_text(pages, chunk_size=512, overlap=64, document_name="multi")
        page_nums = {c["page"] for c in chunks}
        assert 1 in page_nums
        assert 2 in page_nums

    def test_overlap_produces_shared_content(self):
        """With overlap > 0 and enough text, consecutive chunks should share
        some words."""
        text = " ".join([f"w{i}" for i in range(800)])
        pages = self._make_pages([text])
        chunks = chunk_text(pages, chunk_size=128, overlap=32, document_name="ovlp")
        if len(chunks) >= 2:
            words_first = set(chunks[0]["text"].split())
            words_second = set(chunks[1]["text"].split())
            shared = words_first & words_second
            assert len(shared) > 0, "Consecutive chunks should share overlapping words"

    def test_section_detection_numeric(self):
        """A chunk starting with a numeric line should detect it as a section."""
        pages = [{"page": 1, "text": "3.1 Scope of Application\nThis section covers..."}]
        chunks = chunk_text(pages, chunk_size=512, overlap=64, document_name="sec")
        assert chunks[0]["section"] is not None
        assert "3.1" in chunks[0]["section"]

    def test_section_detection_uppercase(self):
        """A chunk starting with an all-caps line should detect it as a section."""
        pages = [{"page": 1, "text": "INTRODUCTION\nThis document provides guidance..."}]
        chunks = chunk_text(pages, chunk_size=512, overlap=64, document_name="sec")
        assert chunks[0]["section"] is not None
        assert "INTRODUCTION" in chunks[0]["section"]

    def test_small_text_single_chunk(self):
        """A small amount of text should produce exactly one chunk."""
        pages = self._make_pages(["Short regulatory note."])
        chunks = chunk_text(pages, chunk_size=512, overlap=64, document_name="small")
        assert len(chunks) == 1
        assert "Short regulatory note." in chunks[0]["text"]


# ---------------------------------------------------------------------------
# ChromaDB client tests -- skipped if chromadb is not installed
# ---------------------------------------------------------------------------

class TestChromaClient:
    """Tests for the ChromaDB vector store client."""

    def test_get_collection_count_fresh(self, monkeypatch):
        """A fresh collection should have count 0."""
        import tempfile
        import shutil
        from pathlib import Path

        chromadb = pytest.importorskip("chromadb")

        # Use tempfile.mkdtemp to avoid pytest tmp_path permission issues on Windows
        temp_dir = Path(tempfile.mkdtemp())
        try:
            import backend.db.chroma_client as chroma_mod

            monkeypatch.setattr(chroma_mod, "_client", None)
            monkeypatch.setattr(chroma_mod, "_collection", None)
            monkeypatch.setattr(chroma_mod, "_PERSIST_DIR", temp_dir / "chroma_test")
            monkeypatch.setattr(
                chroma_mod, "_COLLECTION_NAME", "test_regulatory_docs"
            )

            count = chroma_mod.get_collection_count()
            assert count == 0
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
