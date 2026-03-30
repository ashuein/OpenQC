# Task 03: Sigma Analysis

- Goal: implement Sigma calculation, classification, normalized decision chart outputs, and default rule recommendations
- Primary spec: `docs/specs/03-sigma-analysis.md`
- Allowed secondary specs: `docs/specs/02-qc-westgard.md`, `docs/specs/10-api-and-data-contracts.md`
- Owned modules: `backend/engine/sigma_engine.py`, `backend/models/sigma_schemas.py`, `backend/routers/sigma.py`
- Inputs: assay TEa, bias, CV
- Deliverables: Sigma endpoint, trend endpoint, stable classification logic, NMEDx coordinates
- Dependencies: Task 01
- Acceptance tests: formula tests, boundary classification tests, normalized coordinate tests
- Done definition: Sigma results are suitable for both API use and reporting
- Out of scope: frontend chart rendering
