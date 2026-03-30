# PCR Lab QC — Project Plan Document
**Version:** 2.0  
**Date:** March 27, 2026  
**Stack:** Vue 3 + Vite | Python FastAPI | SQLite | ChromaDB | ECharts | Plotly.js

---

## 1. Project Intent

An open-source, locally deployable web application for clinical and IVD diagnostic laboratories to:

- Monitor PCR quality control data over time using Westgard rules
- Perform assay validation (LOD, precision, linearity) with structured report output
- Analyze analytical performance using Six Sigma metrics
- Maintain a cryptographically verifiable audit trail for regulatory compliance
- Query CDSCO and ICMR regulatory documents via an embedded RAG assistant

**Positioning:** Free, open-source alternative to Westgard Green Belt + Black Belt, with CDSCO/CE-IVD audit trail support and built-in regulatory guidance. Designed for Indian IVD labs underserved by Western-priced QC software.

---

## 2. System Boundaries

### 2.1 In Scope (v1)

- Local deployment only (single machine, single user session)
- Excel file input from any major RT-PCR instrument export
- Westgard rules: 1-2s, 1-3s, 2-2s, R-4s, 4-1s, 10x
- Sigma metric calculation per assay
- NMEDx (Normalized Method Decision Chart)
- Levey-Jennings charting per control level
- Assay validation: LOD, precision (intra/inter-run), linearity
- SHA-256 file hashing + SQLite access/event log with chain integrity
- PDF report export per module
- Reagent lot and control lot tracking
- CDSCO/ICMR regulatory RAG assistant (local, no cloud vector store)

### 2.2 Out of Scope (v1)

- Cloud deployment / multi-user auth
- LIS/LIMS interface
- Microbiology qualitative testing module
- Real-time instrument data ingestion
- LDAP / SSO authentication
- Mobile responsiveness
- LiteParse integration (deferred to Phase 4 revisit for instrument PDF parsing)

---

## 3. User Roles (v1)

| Role | Description |
|---|---|
| Lab Technician | Uploads data, views charts, flags violations |
| Lab Manager | Reviews reports, views audit log, exports PDF |

Single session, no login required for v1. Role distinction is UI-only — both roles access all features.

---

## 4. Feature Specification

### 4.1 QC Monitor

| Feature | Description |
|---|---|
| Excel upload | Accept .xlsx/.xls from QuantStudio, CFX Manager, Roche LC exports |
| Control lot tracking | Tag each upload with reagent lot + control lot |
| Levey-Jennings chart | Per control level (L1, L2, L3), per assay, per channel |
| Westgard rule engine | All 6 core rules, real-time flag on data point |
| Violation log | Per-run list of rule violations with cycle, value, rule triggered |
| Run summary | Pass/fail per run, violation count, mean/SD/CV |
| Multi-run view | Plot last N runs on single chart, toggle lot boundaries |

### 4.2 Sigma Analysis

| Feature | Description |
|---|---|
| TEa input | User-defined Total Allowable Error per assay (%) |
| Bias input | User-defined or calculated from peer group |
| CV input | Calculated from uploaded QC data |
| Sigma score | Formula: (TEa - Bias) / CV |
| Sigma classification | World class (≥6), Excellent (5–6), Good (4–5), Marginal (3–4), Unacceptable (<3) |
| NMEDx chart | All assays plotted on normalized decision chart, color-coded by Sigma band |
| Recommended QC rules | Auto-suggest optimal Westgard rules per Sigma score |

### 4.3 Assay Validator

| Feature | Description |
|---|---|
| LOD calculation | Mean + 3SD of blank / lowest concentration replicates |
| LOQ calculation | Lowest concentration with CV ≤ user-defined threshold |
| Intra-run precision | CV across replicates within single run |
| Inter-run precision | CV across minimum 3 runs over 3 days |
| Linearity | R² and slope across dilution series, deviation from expected |
| Acceptance criteria | User-defined per parameter, pass/fail flagged |
| Validation report | Structured PDF: all parameters, raw data table, pass/fail summary |

### 4.4 Audit Trail

| Feature | Description |
|---|---|
| File hash on upload | SHA-256 of every uploaded file, stored at time of upload |
| Tamper detection | Re-hash on each access, flag if hash differs from stored value |
| Access log | Timestamp, filename, action (upload/view/export), username if set |
| Event log | Report generation, lot changes, settings changes |
| Chain integrity | Each log entry includes SHA-256 of previous entry — simple chain structure |
| Audit log export | Signed JSON export of full log for regulatory submission |

### 4.5 Lot Tracker

| Feature | Description |
|---|---|
| Reagent lot registry | Name, lot number, expiry, open date |
| Control lot registry | Control name, lot number, manufacturer, assigned mean/SD |
| Lot boundary markers | Visible on LJ charts where lot changed |
| Lot change event | Logged in audit trail automatically |

### 4.6 Report Export

| Feature | Description | Format |
|---|---|---|
| QC run report | Single run: LJ chart image + violation list + summary stats | PDF |
| Validation report | Full parameter table + raw data + pass/fail per criterion | PDF |
| Sigma report | NMEDx chart + per-assay Sigma table + recommended rules | PDF |
| Audit log export | Full chronological event log with chain hashes | JSON + PDF |

### 4.7 CDSCO Regulatory RAG Assistant

| Feature | Description |
|---|---|
| Document corpus | CDSCO MD-15, CDSCO IVD performance evaluation guidance, ICMR diagnostic validation guidelines, ISO 15189 summary |
| Query interface | Free-text question input, single-turn Q&A (no conversation history in v1) |
| Answer output | Answer in plain language + source document name + clause/section reference |
| Ingestion pipeline | One-time local ingestion on first run, stored in ChromaDB |
| Retrieval model | Sentence-transformers (local embeddings, no API call for retrieval) |
| Answer model | claude-haiku-4-5 for retrieval ranking, claude-sonnet-4-6 for answer generation |
| Scope guardrail | System prompt restricts answers to ingested documents only — no hallucinated regulatory claims |
| Example queries | "What precision data is required for CDSCO IVD submission?", "How many validation sites are required for multicenter studies?", "What is the LOD acceptance criterion under MD-15?" |

---

## 5. Module Architecture

### 5.1 Backend Modules (FastAPI)

Each module is a separate router file. No business logic in `main.py`. No cross-module imports between engine files.

```
backend/
├── main.py                            # App init, CORS, router registration only
├── routers/
│   ├── qc.py                          # QC monitor endpoints
│   ├── sigma.py                       # Sigma analysis endpoints
│   ├── validation.py                  # Assay validation endpoints
│   ├── audit.py                       # Audit trail endpoints
│   ├── lots.py                        # Lot registry endpoints
│   └── rag.py                         # CDSCO RAG assistant endpoints
├── engine/
│   ├── westgard_rules.py              # Pure rule logic, no I/O, no DB calls
│   ├── sigma_engine.py                # TEa/bias/CV → Sigma score, NMEDx coordinates
│   ├── validation_engine.py           # LOD/LOQ/precision/linearity calculations
│   ├── audit_engine.py                # SHA-256, chain hash, SQLite writer
│   ├── report_engine.py               # PDF generation (WeasyPrint)
│   └── rag_engine.py                  # Chunking, embedding, retrieval, answer generation
├── parsers/
│   ├── base_parser.py                 # Abstract base class, column mapping interface
│   ├── quantstudio_parser.py          # QuantStudio .xlsx format handler
│   ├── cfx_parser.py                  # Bio-Rad CFX .xlsx format handler
│   ├── generic_parser.py              # Fallback: user-mapped column generic Excel
│   └── document_parser.py             # PDF ingestion for RAG: PyMuPDF + pdfplumber
├── models/
│   ├── qc_schemas.py                  # Pydantic: QC data models
│   ├── sigma_schemas.py               # Pydantic: Sigma input/output models
│   ├── validation_schemas.py          # Pydantic: Validation parameter models
│   ├── audit_schemas.py               # Pydantic: Audit log entry models
│   ├── lot_schemas.py                 # Pydantic: Lot registry models
│   └── rag_schemas.py                 # Pydantic: RAG query/response models
├── db/
│   ├── database.py                    # SQLite connection, session management
│   ├── qc_repository.py               # QC run CRUD
│   ├── audit_repository.py            # Audit log CRUD
│   ├── lot_repository.py              # Lot registry CRUD
│   └── chroma_client.py               # ChromaDB client init, collection management
├── data/
│   └── regulatory_docs/               # CDSCO MD-15, ICMR guidelines PDFs stored here
└── utils/
    ├── hasher.py                      # SHA-256 utilities
    ├── stats.py                       # Shared: mean, SD, CV, linear regression
    └── pdf_templates/                 # HTML templates for WeasyPrint
        ├── qc_report.html
        ├── validation_report.html
        ├── sigma_report.html
        └── audit_report.html
```

### 5.2 Frontend Modules (Vue 3)

Each view is a single-responsibility page. Shared state via Pinia store. No store imports between unrelated modules.

```
frontend/
├── src/
│   ├── main.js                        # App init, router, Pinia
│   ├── router/
│   │   └── index.js                   # Route definitions
│   ├── stores/
│   │   ├── qcStore.js                 # QC run data, violation list
│   │   ├── sigmaStore.js              # Sigma inputs + results
│   │   ├── validationStore.js         # Validation run data
│   │   ├── auditStore.js              # Audit log entries
│   │   ├── lotStore.js                # Lot registry state
│   │   └── ragStore.js                # RAG query/response state
│   ├── views/
│   │   ├── DashboardView.vue          # Overview: recent runs, violation summary, quick stats
│   │   ├── QCMonitorView.vue          # LJ charts + Westgard flags
│   │   ├── SigmaView.vue              # NMEDx chart + Sigma table
│   │   ├── ValidatorView.vue          # Assay validation workflow
│   │   ├── AuditView.vue              # Audit log table + export
│   │   ├── LotRegistryView.vue        # Lot management
│   │   └── RegulatoryAssistantView.vue# CDSCO RAG chat interface
│   ├── components/
│   │   ├── charts/
│   │   │   ├── LJChart.vue            # Levey-Jennings (ECharts)
│   │   │   ├── NMEDxChart.vue         # Normalized decision chart (Plotly)
│   │   │   └── LinearityChart.vue     # Linearity regression plot (ECharts)
│   │   ├── upload/
│   │   │   ├── FileDropZone.vue       # Drag-drop Excel uploader
│   │   │   └── UploadProgress.vue     # Upload + parse progress indicator
│   │   ├── tables/
│   │   │   ├── ViolationTable.vue     # Westgard violation list
│   │   │   ├── RunSummaryTable.vue    # Per-run stats summary
│   │   │   ├── ValidationTable.vue    # Validation parameter results
│   │   │   └── AuditTable.vue         # Audit log entries
│   │   ├── forms/
│   │   │   ├── SigmaInputForm.vue     # TEa, bias, CV inputs per assay
│   │   │   ├── LotForm.vue            # Add/edit lot entry
│   │   │   └── AcceptanceForm.vue     # Define acceptance criteria
│   │   ├── rag/
│   │   │   ├── QueryInput.vue         # Question input + submit
│   │   │   ├── AnswerCard.vue         # Answer + source reference display
│   │   │   └── IngestionStatus.vue    # Shows corpus ingestion state on first run
│   │   └── shared/
│   │       ├── StatusBadge.vue        # Pass/Fail/Warning indicator
│   │       ├── ViolationBadge.vue     # Westgard rule label chip
│   │       ├── ExportButton.vue       # PDF export trigger
│   │       └── PageHeader.vue         # Consistent page title + actions bar
│   ├── api/
│   │   ├── qcApi.js                   # QC endpoint calls
│   │   ├── sigmaApi.js                # Sigma endpoint calls
│   │   ├── validationApi.js           # Validation endpoint calls
│   │   ├── auditApi.js                # Audit endpoint calls
│   │   ├── lotApi.js                  # Lot registry endpoint calls
│   │   └── ragApi.js                  # RAG query endpoint calls
│   └── assets/
│       └── styles/
│           └── main.css               # Global styles, CSS variables
```

---

## 6. API Contract

### 6.1 QC Monitor

| Method | Endpoint | Input | Output |
|---|---|---|---|
| POST | `/qc/upload` | Excel file + lot metadata | Parsed run object with Ct values |
| POST | `/qc/analyze` | Run ID | Violation list + LJ coordinates |
| GET | `/qc/runs` | query: assay, date range | List of run summaries |
| GET | `/qc/run/{id}` | run_id | Full run detail |
| DELETE | `/qc/run/{id}` | run_id | Confirmation |

### 6.2 Sigma Analysis

| Method | Endpoint | Input | Output |
|---|---|---|---|
| POST | `/sigma/calculate` | List of {assay, TEa, bias, CV} | Sigma scores + NMEDx coordinates |
| GET | `/sigma/history` | query: assay | Historical Sigma trend |

### 6.3 Assay Validation

| Method | Endpoint | Input | Output |
|---|---|---|---|
| POST | `/validation/upload` | Excel file + validation type | Parsed validation dataset |
| POST | `/validation/run` | Dataset ID + acceptance criteria | LOD/precision/linearity results |
| GET | `/validation/report/{id}` | validation_id | PDF report binary |

### 6.4 Audit Trail

| Method | Endpoint | Input | Output |
|---|---|---|---|
| GET | `/audit/log` | query: date range, event type | Paginated log entries |
| GET | `/audit/verify/{file_hash}` | hash | Match/tamper status |
| GET | `/audit/export` | format: json/pdf | Signed audit log export |

### 6.5 Lot Registry

| Method | Endpoint | Input | Output |
|---|---|---|---|
| GET | `/lots/reagents` | — | All reagent lots |
| POST | `/lots/reagents` | Lot object | Created lot |
| GET | `/lots/controls` | — | All control lots |
| POST | `/lots/controls` | Lot object | Created lot |

### 6.6 RAG Assistant

| Method | Endpoint | Input | Output |
|---|---|---|---|
| GET | `/rag/status` | — | Corpus ingestion state, document count, chunk count |
| POST | `/rag/ingest` | — | Triggers one-time ingestion of regulatory_docs/ folder |
| POST | `/rag/query` | {question: str} | {answer: str, sources: [{doc, section, page}]} |

---

## 7. Data Models (Key Schemas)

### 7.1 QC Run
```
QCRun:
  id: UUID
  uploaded_at: datetime
  file_name: str
  file_hash: str (SHA-256)
  instrument: str
  assay: str
  channel: str
  reagent_lot_id: UUID
  control_lot_id: UUID
  data_points: List[QCDataPoint]

QCDataPoint:
  cycle: int
  control_level: str        (L1 / L2 / L3)
  ct_value: float
  mean: float
  sd: float
  z_score: float
  violations: List[str]     (rule codes e.g. "1-3s", "R-4s")
```

### 7.2 Sigma
```
SigmaInput:
  assay: str
  tea_percent: float
  bias_percent: float
  cv_percent: float

SigmaResult:
  assay: str
  sigma_score: float
  classification: str       (world_class / excellent / good / marginal / unacceptable)
  recommended_rules: List[str]
  nmedx_x: float
  nmedx_y: float
```

### 7.3 Audit Entry
```
AuditEntry:
  id: int (sequential)
  timestamp: datetime
  event_type: str           (upload / view / export / lot_change / settings / rag_query)
  file_name: str | null
  file_hash: str | null
  action_detail: str
  previous_entry_hash: str  (SHA-256 of previous entry — chain integrity)
  entry_hash: str           (SHA-256 of this entry's content)
```

### 7.4 RAG Response
```
RAGQuery:
  question: str

RAGResponse:
  answer: str
  sources: List[RAGSource]
  model_used: str

RAGSource:
  document_name: str
  section: str | null
  page_number: int | null
  chunk_preview: str        (first 100 chars of retrieved chunk)
```

---

## 8. Document Parser Decision

### 8.1 For RAG Ingestion (Regulatory PDFs)

| Tool | Decision | Reason |
|---|---|---|
| **PyMuPDF** | Primary | Fast, reliable text extraction for linear clause-based regulatory PDFs |
| **pdfplumber** | Secondary | Table extraction for MD-15 annexures and structured appendices |
| **LiteParse** | Rejected for this use | TypeScript-native; Python wrapper adds Node.js dependency to FastAPI backend; spatial grid output is irrelevant for linear regulatory text |

### 8.2 LiteParse — Deferred, Not Discarded

LiteParse is the correct tool for parsing **instrument-generated PDF reports** where layout matters (scanned lab reports, chromatogram PDFs, mixed-layout instrument outputs). Revisit for Phase 4 audit trail module if instrument PDF verification is added post-v1.

### 8.3 RAG Stack

```
Ingestion:
  document_parser.py
    → PyMuPDF extracts raw text per page
    → pdfplumber extracts tables per page
    → Combined, clause-boundary-aware chunking
    → Chunk size: 512 tokens, overlap: 64 tokens

Embedding:
  sentence-transformers/all-MiniLM-L6-v2 (local, no API)
  Runs once at ingestion, stored in ChromaDB

Vector Store:
  ChromaDB (local, persistent, zero config, no Docker required)
  One collection per document corpus version

Retrieval:
  Top-5 chunks by cosine similarity
  claude-haiku-4-5 re-ranks retrieved chunks (relevance scoring)

Answer Generation:
  claude-sonnet-4-6
  System prompt: answer only from provided context, cite source + section
  Max tokens: 1024
```

---

## 9. UI Design Principles

- **Color system:** Dark sidebar, light content area. Violation red (#E53935), warning amber (#F9A825), pass green (#43A047), neutral grey (#607D8B)
- **Charts:** ECharts for LJ and linearity (performant for time-series). Plotly for NMEDx (scatter with zone shading)
- **Tables:** Sortable, filterable. Violations highlighted row-level, not just cell
- **No modals for data entry:** Use inline expandable forms or dedicated view routes
- **Export button:** Persistent in page header for every view that has a report
- **Status indicators:** Badge component — not color alone, always includes text label (accessible)
- **RAG view:** Single column, question at top, answer card below, source chips at bottom of card. No chat history UI in v1.

---

## 10. Westgard Rules Reference (Implementation Spec)

| Rule | Trigger Condition | Action |
|---|---|---|
| 1-2s | 1 point > mean ± 2SD | Warning only, do not reject |
| 1-3s | 1 point > mean ± 3SD | Reject run |
| 2-2s | 2 consecutive points > mean + 2SD or < mean - 2SD | Reject run |
| R-4s | 1 point > mean + 2SD AND next < mean - 2SD (range > 4SD) | Reject run |
| 4-1s | 4 consecutive points > mean + 1SD or < mean - 1SD | Reject run |
| 10x | 10 consecutive points on same side of mean | Reject run |

Rules evaluated in listed order. First reject-level violation stops evaluation for that run. 1-2s warning does not stop evaluation.

---

## 11. Build Phases

### Phase 1 — Backend Core (Days 1–2)
- `utils/stats.py` (mean, SD, CV, linear regression — no dependencies)
- `parsers/base_parser.py` + `parsers/quantstudio_parser.py` + `parsers/generic_parser.py`
- `engine/westgard_rules.py` (all 6 rules, pure functions)
- `models/qc_schemas.py` Pydantic models
- `db/database.py` + `db/qc_repository.py`
- `routers/qc.py` (upload + analyze endpoints)
- `main.py` wired, CORS configured
- Validate via Swagger UI at `/docs`

### Phase 2 — QC Frontend (Days 3–4)
- Vue 3 + Vite scaffold, Pinia, Vue Router installed
- `api/qcApi.js`
- `components/upload/FileDropZone.vue` + `UploadProgress.vue`
- `components/charts/LJChart.vue` (ECharts, single control level)
- `components/tables/ViolationTable.vue`
- `stores/qcStore.js`
- `views/QCMonitorView.vue` wiring store + API
- End-to-end test: upload Excel → LJ chart renders + violations listed

### Phase 3 — Sigma + Validation (Days 5–6)
- `engine/sigma_engine.py` + `models/sigma_schemas.py` + `routers/sigma.py`
- `engine/validation_engine.py` + `models/validation_schemas.py` + `routers/validation.py`
- `components/charts/NMEDxChart.vue` (Plotly scatter with Sigma zone shading)
- `components/charts/LinearityChart.vue` (ECharts regression plot)
- `components/forms/SigmaInputForm.vue` + `views/SigmaView.vue`
- `components/tables/ValidationTable.vue` + `views/ValidatorView.vue`

### Phase 4 — Audit Trail (Day 7)
- `utils/hasher.py` (SHA-256, chain hash generation)
- `engine/audit_engine.py`
- `db/audit_repository.py` + `models/audit_schemas.py`
- `routers/audit.py`
- `components/tables/AuditTable.vue` + `views/AuditView.vue`
- Tamper detection test: modify uploaded file → re-verify → flag confirmed

### Phase 5 — Lot Registry + Dashboard (Day 8)
- `db/lot_repository.py` + `models/lot_schemas.py` + `routers/lots.py`
- `components/forms/LotForm.vue` + `views/LotRegistryView.vue`
- Lot boundary marker layer added to `LJChart.vue`
- `views/DashboardView.vue` (recent runs, violation count, Sigma band summary)

### Phase 6 — Report Export (Day 9)
- `engine/report_engine.py` (WeasyPrint)
- `utils/pdf_templates/` — QC, validation, Sigma, audit HTML templates
- `components/shared/ExportButton.vue` wired to all views
- PDF output tested for each module

### Phase 7 — CDSCO RAG Assistant (Days 10–11)
- `parsers/document_parser.py` (PyMuPDF primary, pdfplumber for tables)
- `db/chroma_client.py` (ChromaDB init, collection setup)
- `engine/rag_engine.py`:
  - Ingestion pipeline: parse → chunk → embed → store
  - Retrieval: cosine similarity top-5 → haiku re-rank
  - Answer: sonnet-4-6 with source citation prompt
- `models/rag_schemas.py` + `routers/rag.py`
- `components/rag/QueryInput.vue` + `AnswerCard.vue` + `IngestionStatus.vue`
- `stores/ragStore.js` + `api/ragApi.js`
- `views/RegulatoryAssistantView.vue`
- Regulatory documents added to `backend/data/regulatory_docs/`
- Scope guardrail tested: out-of-corpus question → explicit "not found in documents" response

### Phase 8 — Polish + README (Day 12)
- Modular structure audit: verify no cross-module engine imports
- Sample Excel test files added to `/data`
- Architecture diagram (ASCII or draw.io export)
- README with positioning statement, setup instructions, screenshot
- WeasyPrint / Chromium dependency documented in setup guide
- `docker-compose.yml` stub for future deployment phase

---

## 12. Constraints and Assumptions

| Constraint | Detail |
|---|---|
| Excel format | Assumes instrument exports Ct value column + control level column. Column mapping configurable in settings for generic parser |
| Control statistics | Mean and SD calculated from first 20 data points per lot, then fixed. User can override |
| LOD method | Mean + 3SD of blank replicates. Probit analysis deferred to post-v1 |
| Linearity | Simple linear regression R² only. Polynomial fit not in v1 |
| Audit chain | SQLite — not tamper-proof at OS level. Sufficient for CDSCO documentation, not for FDA 21 CFR Part 11 full compliance |
| Single user | No concurrent session handling. SQLite + ChromaDB sufficient |
| PDF generation | WeasyPrint requires Chromium or wkhtmltopdf — documented in setup |
| RAG corpus | Fixed document set, manually curated. No dynamic document addition in v1 |
| RAG embeddings | sentence-transformers runs on CPU. First-run ingestion may take 2–5 minutes for full corpus |
| RAG answers | Restricted to ingested documents by system prompt. Model may still hallucinate clause numbers — output should be treated as guidance, not legal interpretation |

---

## 13. README Positioning (Draft)

```
An open-source alternative to Westgard Green Belt + Black Belt for 
PCR diagnostic laboratories — Levey-Jennings charting, full Westgard 
rule implementation, Six Sigma analysis, assay validation reporting, 
cryptographic audit logging for CDSCO/CE-IVD compliance, and a 
built-in regulatory assistant trained on CDSCO and ICMR guidelines. 
Free, local, no subscription.
```

---

## 14. Future Scope (Post v1)

- Multi-user with role-based access (Lab Manager / Technician)
- Cloud deployment (Docker Compose → managed VPS)
- LIS integration (HL7 2.x export)
- Microbiology qualitative QC module
- Probit LOD analysis
- Peer group comparison (anonymized cross-lab benchmarking)
- Instrument drift detection (regression on control Ct over time)
- LiteParse integration for instrument-generated PDF report verification in audit trail
- RAG conversation history (multi-turn)
- RAG document upload via UI (user-added regulatory documents)
- ISO 15189 accreditation checklist module
