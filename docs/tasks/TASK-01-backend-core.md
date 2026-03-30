# Task 01: Backend Core

- Goal: scaffold FastAPI foundation, SQLite session management, parser base classes, and shared stats utilities
- Primary spec: `docs/specs/01-backend-core.md`
- Allowed secondary specs: `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md`
- Owned modules: `backend/main.py`, `backend/db/database.py`, `backend/parsers/base_parser.py`, `backend/utils/stats.py`
- Inputs: project plan, backend core spec
- Deliverables: running FastAPI app skeleton, registered routers, parser base contract, tested stats helpers
- Dependencies: none
- Acceptance tests: app boots, router registration works, stats helpers are unit-tested, parser interface can be subclassed
- Done definition: foundational backend files exist and domain teams can build on them without redefining app setup
- Out of scope: module-specific calculations, UI payload formatting
