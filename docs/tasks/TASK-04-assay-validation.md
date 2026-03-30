# Task 04: Assay Validation

- Goal: implement validation dataset handling and calculations for LOD, LOQ, precision, and linearity
- Primary spec: `docs/specs/04-assay-validation.md`
- Allowed secondary specs: `docs/specs/10-api-and-data-contracts.md`
- Owned modules: `backend/engine/validation_engine.py`, `backend/models/validation_schemas.py`, `backend/routers/validation.py`
- Inputs: parsed validation datasets, user acceptance criteria
- Deliverables: upload endpoint, run endpoint, canonical output structure for reporting
- Dependencies: Task 01
- Acceptance tests: formula tests for each mode, threshold pass/fail tests, sparse data rejection cases
- Done definition: validation outputs are deterministic and report-ready
- Out of scope: PDF template implementation
