# Task 07: Reporting

- Goal: implement PDF and JSON export assembly for QC, validation, Sigma, and audit modules
- Primary spec: `docs/specs/07-reporting.md`
- Allowed secondary specs: `docs/specs/02-qc-westgard.md`, `docs/specs/03-sigma-analysis.md`, `docs/specs/04-assay-validation.md`, `docs/specs/05-audit-trail.md`
- Owned modules: `backend/engine/report_engine.py`, report templates, export routes
- Inputs: stored domain outputs and chart payloads
- Deliverables: report templates, rendering pipeline, export integration
- Dependencies: Tasks 02-05
- Acceptance tests: each report renders from stored outputs, audit export includes verification metadata, export events are logged
- Done definition: all module exports are reproducible and stable
- Out of scope: redesigning domain calculations
