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
                             ┌──────────── Design Workflow ────────────┐
                             │ Figma screen spec ──▶ UI implementation │
                             └──────────────────────┬──────────────────┘
                                                    │
┌──────────────────────────── Frontend (Vue 3 + Vite) ────────────────────────────┐
│ App Shell │ Views │ shadcn-vue Primitives │ Stores │ API Clients │ Charts       │
└───────────────────────────────┬─────────────────────────────────────────────────┘
                                │ HTTP/JSON
┌───────────────────────────────▼─────────────────────────────────────────────────┐
│ FastAPI Routers                                                                 │
│ qc │ sigma │ validation │ audit │ lots │ rag                                    │
└───────────────┬───────────────────────┬───────────────────────┬─────────────────┘
                │                       │                       │
        ┌───────▼───────┐      ┌────────▼────────┐      ┌──────▼────────┐
        │ Engines        │      │ Parsers          │      │ Report Engine │
        │ westgard       │      │ instrument .xlsx │      │ PDF rendering │
        │ sigma          │      │ generic .xlsx    │      └───────────────┘
        │ validation     │      │ regulatory .pdf  │
        │ audit          │      └────────┬─────────┘
        │ rag            │               │
        └───────┬────────┘       ┌───────▼────────┐
                │                │ Regulatory Docs │
                │                │ local PDF corpus│
                │                └────────────────┘
        ┌───────▼───────────┐
        │ Repositories / DB │
        │ SQLite            │
        │ ChromaDB          │
        └───────────────────┘
```

## Getting Started

### Prerequisites

- **Python 3.12+** — [python.org/downloads](https://www.python.org/downloads/)
- **Node.js 18+** and **npm 9+** — [nodejs.org](https://nodejs.org/)
- **Git** — [git-scm.com](https://git-scm.com/)

### 1. Clone the repository

```bash
git clone https://github.com/ashuein/OpenQC.git
cd OpenQC
```

### 2. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

This installs the core stack (FastAPI, SQLAlchemy, Pydantic, openpyxl). Optional heavy dependencies for specific features can be added later — see the table below.

### 3. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Start development servers

Open two terminals from the project root:

**Terminal 1 — Backend API:**
```bash
uvicorn backend.main:app --reload --port 8000
```

The database (`backend/data/openqc.db`) is created automatically on first startup.

**Terminal 2 — Frontend dev server:**
```bash
cd frontend
npm run dev
```

### 5. Open the app

- **Frontend UI:** http://localhost:5173
- **Backend Swagger docs:** http://localhost:8000/docs
- **Health check:** http://localhost:8000/

### 6. Try it with sample data

Sample Excel files are included in `backend/data/samples/`. Upload `sample_qc_violations.xlsx` through the QC Monitor to see Westgard violation detection in action.

To regenerate sample files:
```bash
python backend/data/samples/generate_samples.py
```

### Optional Dependencies

The core app runs without these. Install as needed for specific features:

| Feature | Package | Install | Notes |
|---------|---------|---------|-------|
| PDF Reports | WeasyPrint | `pip install weasyprint` | Requires system GTK libraries ([setup guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)) |
| RAG Ingestion | PyMuPDF, pdfplumber | `pip install PyMuPDF pdfplumber` | For parsing regulatory PDFs |
| RAG Embeddings | sentence-transformers | `pip install sentence-transformers` | ~500 MB download, runs on CPU |
| RAG Answers | Anthropic SDK | `pip install anthropic` | Set `ANTHROPIC_API_KEY` env var |
| Vector Store | ChromaDB | `pip install chromadb` | Local persistent store |

### RAG Setup (optional)

To use the Regulatory Assistant:

1. Place regulatory PDFs (CDSCO MD-15, ICMR guidelines, etc.) in `backend/data/regulatory_docs/`
2. Install RAG dependencies: `pip install PyMuPDF pdfplumber chromadb sentence-transformers anthropic`
3. Set your API key: `export ANTHROPIC_API_KEY=sk-ant-...`
4. Start the backend and click **Ingest Documents** in the Regulatory Assistant view (one-time, 2-5 min on CPU)

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

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Future Scope

- Multi-user with role-based access
- Docker Compose deployment
- LIS/LIMS integration (HL7 2.x)
- Probit LOD analysis
- Peer group comparison
- Instrument drift detection
- Multi-turn RAG conversation
