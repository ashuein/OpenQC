# Task 06: Lot Tracker

- Goal: implement reagent and control lot registries plus QC boundary behavior
- Primary spec: `docs/specs/06-lot-tracker.md`
- Allowed secondary specs: `docs/specs/02-qc-westgard.md`, `docs/specs/10-api-and-data-contracts.md`
- Owned modules: `backend/models/lot_schemas.py`, `backend/db/lot_repository.py`, `backend/routers/lots.py`
- Inputs: lot creation/update requests
- Deliverables: lot CRUD endpoints, canonical lot records, boundary metadata for QC views
- Dependencies: Task 01
- Acceptance tests: lot records persist correctly, duplicate scope checks work, lot changes are audit-visible
- Done definition: lot metadata is available to QC, reporting, and UI layers
- Out of scope: LIS integration
