# Task 05: Audit Trail

- Goal: implement file hashing, chained audit entries, verification workflows, and audit exports
- Primary spec: `docs/specs/05-audit-trail.md`
- Allowed secondary specs: `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md`
- Owned modules: `backend/engine/audit_engine.py`, `backend/models/audit_schemas.py`, `backend/db/audit_repository.py`, `backend/routers/audit.py`
- Inputs: upload, view, export, lot change, settings, and RAG events
- Deliverables: append-only chain, verification endpoint, export endpoint
- Dependencies: Task 01
- Acceptance tests: chain validation passes on untouched data, tamper detection identifies first bad entry, export logs itself
- Done definition: audit chain is reproducible and externally verifiable
- Out of scope: OS-level immutability guarantees
