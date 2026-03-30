# Task 08: Regulatory RAG

- Goal: implement local regulatory document ingestion, retrieval, reranking, and cited answer generation
- Primary spec: `docs/specs/08-regulatory-rag.md`
- Allowed secondary specs: `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md`
- Owned modules: `backend/parsers/document_parser.py`, `backend/db/chroma_client.py`, `backend/engine/rag_engine.py`, `backend/models/rag_schemas.py`, `backend/routers/rag.py`
- Inputs: local regulatory PDFs, user questions
- Deliverables: ingestion workflow, status endpoint, query endpoint, constrained answer output
- Dependencies: Task 01
- Acceptance tests: ingestion creates searchable chunks, out-of-corpus questions fail safely, source citations are always included
- Done definition: regulatory assistant works locally and stays inside corpus scope
- Out of scope: multi-turn conversation history
