# Task 02: QC and Westgard

- Goal: implement QC upload/analyze flow, canonical QC models, and the full Westgard engine with test vectors
- Primary spec: `docs/specs/02-qc-westgard.md`
- Allowed secondary specs: `docs/specs/06-lot-tracker.md`, `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md`
- Owned modules: `backend/routers/qc.py`, `backend/engine/westgard_rules.py`, `backend/models/qc_schemas.py`, `backend/db/qc_repository.py`
- Inputs: parser output, assay configuration, lot metadata
- Deliverables: QC ingestion route, analysis route, complete rule engine, unit-test matrix for all six rules
- Dependencies: Task 01
- Acceptance tests: single-control assays do not trigger `R-4s`, lot resets break multirule chains, full violation capture is recorded, boundary tests pass
- Done definition: QC run analysis is deterministic and fully traceable to the QC spec
- Out of scope: Sigma and PDF report generation
