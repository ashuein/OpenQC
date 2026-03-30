# Spec 08: Regulatory RAG

| Field | Value |
|---|---|
| Spec ID | 08 |
| Purpose | Define local regulatory document ingestion, retrieval, reranking, and answer generation |
| Primary tasks | `docs/tasks/TASK-08-regulatory-rag.md` |
| Owned modules | `backend/parsers/document_parser.py`, `backend/db/chroma_client.py`, `backend/engine/rag_engine.py`, `backend/models/rag_schemas.py`, `backend/routers/rag.py` |
| Allowed secondary specs | `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md` |

## Corpus

The initial corpus contains:

- CDSCO MD-15
- CDSCO IVD performance evaluation guidance
- ICMR diagnostic validation guidance
- ISO 15189 summary material

## Ingestion Rules

- Parse regulatory PDFs locally
- Use PyMuPDF as primary text extraction
- Use pdfplumber for table extraction where needed
- Chunk on clause boundaries when possible
- Target chunk size: `512 tokens`
- Chunk overlap: `64 tokens`

## Retrieval Rules

- Embedding model: local sentence-transformer
- Vector store: local persistent ChromaDB
- Retrieve top 5 by similarity
- Re-rank retrieved chunks before answer generation

## Answer Rules

- Answer only from retrieved corpus context
- Return plain-language answer plus cited sources
- If answer is not supported by retrieved corpus, say so explicitly
- No multi-turn memory in v1

## Output

- `answer`
- `sources[]` with document name, section if known, page number if known, and chunk preview
- `model_used`

## Acceptance Criteria

- First-run ingestion status is queryable
- Out-of-corpus questions return explicit insufficiency, not hallucinated policy
- Source references are always returned when answer text is returned
