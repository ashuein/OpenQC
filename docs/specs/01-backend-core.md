# Spec 01: Backend Core

| Field | Value |
|---|---|
| Spec ID | 01 |
| Purpose | Define backend skeleton, foundational utilities, parser base contracts, and repository/session rules |
| Primary tasks | `docs/tasks/TASK-01-backend-core.md` |
| Owned modules | `backend/main.py`, `backend/db/database.py`, parser base contracts, shared stats utilities |
| Allowed secondary specs | `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md` |

## Purpose

This spec defines the foundational backend shape that every module builds on.

## Owns

- FastAPI application setup
- Router registration
- CORS and local dev settings
- SQLite session lifecycle
- Shared stats helpers
- Parser base interfaces
- Common repository patterns

## Does Not Own

- Westgard rule semantics
- Sigma or validation formulas
- Audit chain rules
- User-facing payload contracts

## Application Structure

- `backend/main.py` initializes FastAPI and registers routers only.
- `backend/db/database.py` exposes engine/session creation and transaction helpers.
- `backend/parsers/base_parser.py` defines the abstract parser interface.
- `backend/utils/stats.py` provides deterministic `mean`, `sd`, `cv`, and linear regression helpers.

## Parser Base Contract

Each parser must expose:

- `can_handle(file_metadata) -> bool`
- `parse(file_bytes, mapping_config | None) -> ParsedDataset`
- `normalize_instrument_name() -> str`

Each parser returns canonical structures, never UI-formatted objects.

## Repository Rules

- Repositories accept canonical data objects only.
- Repositories own CRUD, filtering, and pagination.
- Repositories do not calculate QC or validation decisions.
- Transactions are explicit at the service or router boundary.

## Acceptance Criteria

- FastAPI app boots with all routers registered.
- Shared stats helpers are covered by unit tests.
- Parser interface is reusable by QuantStudio, CFX, and generic parsers.
- Session creation and teardown are centralized.
