# OpenQC

An open-source alternative to Westgard Green Belt + Black Belt for PCR diagnostic laboratories -- Levey-Jennings charting, full Westgard rule implementation, Six Sigma analysis, assay validation reporting, cryptographic audit logging for CDSCO/CE-IVD compliance, and a built-in regulatory assistant trained on CDSCO and ICMR guidelines. Free, local, no subscription.

## Features

- **QC Monitor** -- Upload Excel exports from QuantStudio, CFX Manager, and other PCR instruments. Apply all 6 Westgard rules (1-2s, 1-3s, 2-2s, R-4s, 4-1s, 10x) with real-time violation detection and Levey-Jennings charting.
- **Sigma Analysis** -- Calculate Six Sigma metrics per assay, plot NMEDx normalized decision charts, and get automatic QC rule recommendations based on sigma performance.
- **Assay Validation** -- LOD, LOQ, intra/inter-run precision, and linearity calculations with user-defined acceptance criteria and structured pass/fail reporting.
- **Audit Trail** -- SHA-256 file hashing on upload, hash-chain integrity verification, tamper detection, and signed JSON/PDF audit exports for CDSCO compliance.
- **Lot Tracker** -- Reagent and control lot registries with expiry tracking and automatic Westgard history reset on lot change.
- **Report Export** -- PDF reports for QC runs, validation, sigma analysis, and audit trail via WeasyPrint.
- **Regulatory Assistant** -- Query CDSCO MD-15, ICMR, and ISO 15189 guidance documents through a local RAG pipeline with cited source references.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + Vite, Pinia, Vue Router, Tailwind CSS v4, shadcn-vue primitives (radix-vue), ECharts, Plotly.js |
| Backend | Python FastAPI, SQLAlchemy, Pydantic v2 |
| Storage | SQLite (structured data), ChromaDB (RAG embeddings) |
| PDF Export | WeasyPrint + Jinja2 templates |
| RAG Pipeline | PyMuPDF, pdfplumber, sentence-transformers, Anthropic Claude API |

## Architecture

```text
                             +------------ Design Workflow ------------+
                             | Figma screen spec --> UI implementation  |
                             +--------------------+---------------------+
                                                  |
+---------------------------- Frontend (Vue 3 + Vite) ----------------------------+
| App Shell | Views | shadcn-vue Primitives | Stores | API Clients | Charts      |
+-------------------------------+-------------------------------------------------+
                                | HTTP/JSON
+-------------------------------v-------------------------------------------------+
| FastAPI Routers                                                                  |
| qc | sigma | validation | audit | lots | rag                                    |
+---------------+---------------------+---------------------+---------------------+
                |                     |                     |
        +-------v-------+    +-------v--------+    +-------v-------+
        | Engines        |    | Parsers        |    | Report Engine |
        | westgard       |    | instrument xlsx|    | PDF rendering |
        | sigma          |    | generic xlsx   |    +---------------+
        | validation     |    | regulatory pdf |
        | audit          |    +-------+--------+
        | rag            |            |
        +-------+--------+    +------v---------+
                |              | Regulatory Docs |
                |              | local PDF corpus|
                |              +----------------+
      +---------v---------+
      | Repositories / DB |
      | SQLite            |
      | ChromaDB          |
      +-------------------+
```

## Prerequisites

- Python 3.12+
- Node.js 18+
- npm 9+

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

### Run Development Servers

**Backend** (from project root):
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend** (from frontend/):
```bash
cd frontend
npm run dev
```

The app will be available at http://localhost:5173 with the API at http://localhost:8000.

### Optional Dependencies

The `requirements.txt` includes all packages, but several are only needed for specific features. If you want a minimal install, start with the core and add these as needed:

| Feature | Package | Install |
|---------|---------|---------|
| PDF Reports | WeasyPrint | `pip install weasyprint` (requires system GTK libraries) |
| RAG Ingestion | PyMuPDF, pdfplumber | `pip install PyMuPDF pdfplumber` |
| RAG Embeddings | sentence-transformers | `pip install sentence-transformers` |
| RAG Answers | Anthropic SDK | `pip install anthropic` (requires `ANTHROPIC_API_KEY` env var) |
| Vector Store | ChromaDB | `pip install chromadb` |

## API Documentation

With the backend running, visit http://localhost:8000/docs for the interactive Swagger UI.

## Project Structure

```
OpenQC/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── routers/             # API endpoint handlers
│   ├── engine/              # Pure business logic
│   ├── parsers/             # Excel/PDF file parsers
│   ├── models/              # Pydantic schemas + SQLAlchemy ORM
│   ├── db/                  # Database + ChromaDB clients
│   ├── utils/               # Stats, hashing, PDF templates
│   ├── data/                # SQLite DB, regulatory docs, samples
│   └── tests/               # pytest test suite
├── frontend/
│   ├── src/
│   │   ├── views/           # Page components
│   │   ├── components/      # Reusable UI components
│   │   ├── stores/          # Pinia state management
│   │   ├── api/             # Backend API clients
│   │   └── router/          # Vue Router config
│   └── ...
└── docs/
    ├── ARCHITECTURE.md       # System design
    ├── AI-ROUTING.md         # Agent routing guide
    └── specs/                # Feature specifications
```

## Running Tests

```bash
# Backend tests
python -m pytest backend/tests/ -v

# Frontend build check
cd frontend
npm run build
```

## Westgard Rules Reference

| Rule | Trigger | Action |
|------|---------|--------|
| 1-2s | 1 point > mean +/- 2SD | Warning |
| 1-3s | 1 point > mean +/- 3SD | Reject |
| 2-2s | 2 consecutive > mean +/- 2SD (same side) | Reject |
| R-4s | Within-run spread > 4SD | Reject |
| 4-1s | 4 consecutive > mean +/- 1SD (same side) | Reject |
| 10x | 10 consecutive same side of mean | Reject |

## Design Principles

- Local-first: runs entirely on a single workstation, no cloud required
- Module isolation: engines don't import each other
- Docs-first: specs define behavior, code follows
- Clinical aesthetic: dark theme, grayscale base, semantic colors for QC status only

## License

[To be determined]

## Future Scope

- Multi-user with role-based access
- Docker Compose deployment
- LIS/LIMS integration (HL7 2.x)
- Probit LOD analysis
- Peer group comparison
- Instrument drift detection
- Multi-turn RAG conversation
