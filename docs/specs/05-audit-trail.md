# Spec 05: Audit Trail

| Field | Value |
|---|---|
| Spec ID | 05 |
| Purpose | Define audit entry schema, hash chain behavior, tamper checks, and export rules |
| Primary tasks | `docs/tasks/TASK-05-audit-trail.md` |
| Owned modules | `backend/engine/audit_engine.py`, `backend/models/audit_schemas.py`, `backend/db/audit_repository.py`, `backend/routers/audit.py` |
| Allowed secondary specs | `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md` |

## Event Types

- `upload`
- `view`
- `export`
- `lot_change`
- `settings`
- `rag_query`

## Entry Structure

Each entry must contain:

- sequential ID
- timestamp
- event type
- file name if applicable
- file hash if applicable
- action detail
- previous entry hash
- entry hash

## Hash Rules

- File uploads compute SHA-256 at ingest time
- Entry hash is calculated from the serialized entry payload plus previous entry hash
- First entry uses a fixed genesis value
- Verification recomputes hashes in sequence

## Tamper Detection

- File tamper check compares current file hash to stored upload hash
- Chain tamper check recomputes `entry_hash` values across the full log
- Any mismatch returns a `tamper_detected` result with failing entry ID

## Export Rules

- JSON export includes all fields needed to verify the chain externally
- PDF export includes chronology, summary, and verification outcome
- Export actions themselves must be logged

## Acceptance Criteria

- Sequential inserts preserve chain linkage
- Verification pinpoints the first broken entry
- Re-verification of untouched data passes cleanly
