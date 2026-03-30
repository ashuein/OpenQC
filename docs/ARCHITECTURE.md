# OpenQC Architecture

## Purpose

This document defines the whole-system software design for OpenQC. It is the source of truth for subsystem boundaries, runtime flow, storage responsibilities, and the design-time workflow that links Figma-approved screens to frontend implementation.

## System Goals

- Local-first PCR QC platform for a single laboratory workstation
- Deterministic QC, Sigma, validation, audit, lot tracking, reporting, and regulatory assistant modules
- Low-friction local deployment with SQLite and ChromaDB
- Explicit module boundaries so AI agents and engineers can work independently
- Docs-first implementation process where the frontend is designed in Figma before code

## Architectural Rules

- `backend/main.py` owns app initialization, CORS, and router registration only.
- Business logic lives in `backend/engine/`.
- File parsing lives in `backend/parsers/`.
- Persistence logic lives in `backend/db/`.
- Shared math and hashing helpers live in `backend/utils/`.
- Frontend views remain page-scoped; cross-view state goes through Pinia stores.
- Engine modules do not import each other directly.
- User-facing visual rules are owned only by `docs/specs/09-frontend-ui.md`.
- QC rule semantics are owned only by `docs/specs/02-qc-westgard.md`.

## Canonical Diagram

```text
                             ┌──────────── Design Workflow ────────────┐
                             │ Figma screen spec ──> UI implementation │
                             └──────────────────────┬──────────────────┘
                                                    │
┌──────────────────────────── Frontend (Vue 3 + Vite) ────────────────────────────┐
│ App Shell │ Views │ shadcn-vue Primitives │ Stores │ API Clients │ Charts      │
└───────────────────────────────┬──────────────────────────────────────────────────┘
                                │ HTTP/JSON
┌───────────────────────────────▼──────────────────────────────────────────────────┐
│ FastAPI Routers                                                                  │
│ qc | sigma | validation | audit | lots | rag                                    │
└───────────────┬───────────────────────┬───────────────────────┬─────────────────┘
                │                       │                       │
        ┌───────▼───────┐      ┌────────▼────────┐      ┌──────▼────────┐
        │ Engines       │      │ Parsers         │      │ Report Engine │
        │ westgard      │      │ instrument xlsx │      │ PDF rendering │
        │ sigma         │      │ generic xlsx    │      └───────────────┘
        │ validation    │      │ regulatory pdf  │
        │ audit         │      └────────┬────────┘
        │ rag           │               │
        └───────┬───────┘               │
                │               ┌───────▼────────┐
                │               │ Regulatory Docs │
                │               │ local PDF corpus│
                │               └─────────────────┘
      ┌─────────▼─────────┐
      │ Repositories / DB │
      │ SQLite            │
      │ ChromaDB          │
      └───────────────────┘
```

## Runtime Flow

### Frontend to Backend

1. A view triggers a store action.
2. The store calls a dedicated API client.
3. The API client calls one FastAPI router.
4. The router validates input through Pydantic models.
5. The router delegates to one engine or repository-facing workflow.
6. The router returns a contract defined in `docs/specs/10-api-and-data-contracts.md`.

### QC and Validation Data Flow

1. User uploads an Excel file.
2. Router chooses the parser based on instrument or generic mapping.
3. Parser normalizes rows into canonical internal structures.
4. Engine calculates rule results, statistics, or validation metrics.
5. Repository persists run metadata and derived outputs.
6. Frontend renders charts, tables, and run summaries from canonical payloads.

### Report Flow

1. A module requests a report payload.
2. Domain engine assembles summary data and raw sections.
3. Report engine injects the data into HTML templates.
4. WeasyPrint generates PDF output.
5. Audit trail records the export event and hash chain entry.

### Audit Flow

1. Upload, access, export, lot change, and settings events generate audit entries.
2. Each entry stores the previous hash and its own entry hash.
3. File verification re-hashes on access and compares with the stored upload hash.
4. Audit exports include full chronology and chain integrity metadata.

### Regulatory RAG Flow

1. Regulatory PDFs are stored locally.
2. Ingestion parses each page and extracts tables when needed.
3. Clause-aware chunks are embedded and stored in ChromaDB.
4. Query router retrieves top candidates and re-ranks them.
5. Answer generation is constrained to retrieved context with cited sources.

## Storage Responsibilities

| Store | Ownership |
|---|---|
| SQLite | QC runs, lot registry, audit logs, validation artifacts, settings metadata |
| ChromaDB | Regulatory document embeddings and chunk metadata |
| Local file system | Uploaded files, regulatory PDFs, generated sample data, report templates |

## Frontend Design-Time Workflow

1. Each major screen is specified in Figma before coding.
2. The Figma artifact defines layout, token usage, and component inventory.
3. Implementation follows the approved frame, not ad hoc design choices.
4. UI code uses `Vue 3 + Vite` and `shadcn-vue`-style primitives under the rules in `docs/specs/09-frontend-ui.md`.
5. Any visual deviation requires updating the Figma spec and frontend spec, not improvising in component code.

## Acceptance Criteria

- Every subsystem can be assigned to one primary spec and one task packet.
- No layer owns responsibilities from another layer.
- Both runtime and design workflow are represented.
- Diagram and prose tell the same story.
