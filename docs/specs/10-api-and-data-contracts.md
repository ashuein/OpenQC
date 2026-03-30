# Spec 10: API and Data Contracts

| Field | Value |
|---|---|
| Spec ID | 10 |
| Purpose | Define canonical request and response contracts, IDs, timestamps, errors, and export content types |
| Primary tasks | used as secondary contract source by most tasks |
| Owned modules | Pydantic wire schemas, endpoint request/response definitions |
| Allowed secondary specs | `docs/ARCHITECTURE.md` |

## Global Rules

- IDs are UUIDs unless an audit entry explicitly uses a sequential integer ID
- Timestamps use ISO 8601 UTC strings
- Dates use `YYYY-MM-DD`
- Percentages are numeric values, not strings
- Errors return `{ code, message, details? }`

## Endpoint Contracts

### QC

- `POST /qc/upload`
  - input: multipart file plus lot metadata
  - output: parsed run object with canonical QC points
- `POST /qc/analyze`
  - input: `run_id`
  - output: `run_status`, `first_reject_rule`, `violations`, chart payload, summary stats
- `GET /qc/runs`
  - output: paginated list of run summaries
- `GET /qc/run/{id}`
  - output: full run detail
- `DELETE /qc/run/{id}`
  - output: confirmation object

### Sigma

- `POST /sigma/calculate`
  - input: list of Sigma inputs
  - output: per-assay Sigma results and NMEDx coordinates
- `GET /sigma/history`
  - output: chronological sigma trend for one assay

### Validation

- `POST /validation/upload`
  - input: file and validation type
  - output: parsed validation dataset
- `POST /validation/run`
  - input: dataset ID and acceptance criteria
  - output: validation results and pass/fail summary
- `GET /validation/report/{id}`
  - output: PDF binary

### Audit

- `GET /audit/log`
  - output: paginated audit entries
- `GET /audit/verify/{file_hash}`
  - output: file or chain verification status
- `GET /audit/export`
  - output: JSON or PDF depending on query param

### Lots

- `GET /lots/reagents`
- `POST /lots/reagents`
- `GET /lots/controls`
- `POST /lots/controls`

### RAG

- `GET /rag/status`
- `POST /rag/ingest`
- `POST /rag/query`

## Pagination

- Use `page`, `page_size`, `total`
- Default server-side sort order is newest first unless endpoint states otherwise

## Content Types

- JSON endpoints return `application/json`
- PDF exports return `application/pdf`
- Audit JSON export returns `application/json`

## Acceptance Criteria

- Contract names are stable and shared by backend and frontend
- UI tasks do not invent payload shapes outside this spec
