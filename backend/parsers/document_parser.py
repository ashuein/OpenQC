"""Regulatory document PDF parser for RAG ingestion."""
from pathlib import Path

# Use try/except for optional dependencies
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


def extract_text_pymupdf(pdf_path: str | Path) -> list[dict]:
    """Extract text from PDF using PyMuPDF.

    Returns: list of {"page": int, "text": str} for each page.
    """
    if fitz is None:
        raise ImportError(
            "PyMuPDF (fitz) is required for document parsing. "
            "Install with: pip install PyMuPDF"
        )

    pages = []
    doc = fitz.open(str(pdf_path))
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        if text.strip():
            pages.append({"page": page_num + 1, "text": text})
    doc.close()
    return pages


def extract_tables_pdfplumber(pdf_path: str | Path) -> list[dict]:
    """Extract tables from PDF using pdfplumber.

    Returns: list of {"page": int, "tables": list[list[list[str]]]}
    """
    if pdfplumber is None:
        raise ImportError(
            "pdfplumber is required for table extraction. "
            "Install with: pip install pdfplumber"
        )

    results = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                results.append({"page": i + 1, "tables": tables})
    return results


def chunk_text(
    pages: list[dict],
    chunk_size: int = 512,
    overlap: int = 64,
    document_name: str = "",
) -> list[dict]:
    """Split extracted pages into overlapping chunks.

    Uses approximate token count (words / 0.75).
    Tries to split on clause/section boundaries (lines starting with numbers
    or section headers).

    Returns: list of {
        "text": str,
        "document_name": str,
        "page": int,
        "chunk_index": int,
        "section": str|None  (detected section header if any)
    }
    """
    chunks = []
    chunk_index = 0

    for page_data in pages:
        page_num = page_data["page"]
        text = page_data["text"]
        lines = text.split("\n")
        words = text.split()

        if not words:
            continue

        # Approximate tokens (1 token ~ 0.75 words)
        def token_estimate(w_list: list[str]) -> int:
            return int(len(w_list) / 0.75)

        i = 0
        while i < len(words):
            end = i
            # Advance until we hit chunk_size tokens
            while end < len(words) and token_estimate(words[i:end]) < chunk_size:
                end += 1

            chunk_words = words[i:end]
            chunk_text_str = " ".join(chunk_words)

            # Try to detect section header from the original text lines
            # that overlap with this chunk's content
            section = _detect_section(chunk_text_str, lines)

            chunks.append({
                "text": chunk_text_str,
                "document_name": document_name,
                "page": page_num,
                "chunk_index": chunk_index,
                "section": section,
            })
            chunk_index += 1

            # If we consumed all remaining words, stop
            if end >= len(words):
                break

            # Move forward by (chunk_size - overlap) tokens worth of words
            overlap_words = int(overlap * 0.75)
            i = max(i + 1, end - overlap_words)

    return chunks


def _detect_section(chunk_text_str: str, original_lines: list[str]) -> str | None:
    """Detect section header from original source lines matching chunk content.

    Checks the first few words of the chunk against original document lines
    to find section-like headers (numbered or ALL-CAPS lines).
    """
    # Get the first few words of the chunk to locate it in original lines
    first_words = chunk_text_str.split()[:6]
    if not first_words:
        return None
    first_phrase = " ".join(first_words)

    # Find which original lines overlap with the beginning of this chunk
    for line in original_lines:
        stripped = line.strip()
        if not stripped or len(stripped) >= 100:
            continue
        # Check if this line's content appears near the start of the chunk
        line_words = stripped.split()
        if not line_words:
            continue
        line_phrase = " ".join(line_words)
        if line_phrase in chunk_text_str[:200]:
            if stripped[0].isdigit() or (
                stripped.upper() == stripped and len(stripped) > 1
            ):
                return stripped

    return None


def parse_document(pdf_path: str | Path) -> list[dict]:
    """Full document parsing pipeline: extract text + chunk.

    Returns list of chunks ready for embedding.
    """
    path = Path(pdf_path)
    pages = extract_text_pymupdf(path)
    chunks = chunk_text(pages, document_name=path.stem)
    return chunks
