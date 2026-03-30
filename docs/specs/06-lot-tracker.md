# Spec 06: Lot Tracker

| Field | Value |
|---|---|
| Spec ID | 06 |
| Purpose | Define reagent and control lot registries, field requirements, and QC boundary behavior |
| Primary tasks | `docs/tasks/TASK-06-lot-tracker.md` |
| Owned modules | `backend/models/lot_schemas.py`, `backend/db/lot_repository.py`, `backend/routers/lots.py` |
| Allowed secondary specs | `docs/specs/02-qc-westgard.md`, `docs/specs/10-api-and-data-contracts.md` |

## Reagent Lot Fields

- lot ID
- assay or product name
- lot number
- expiry date
- open date
- status

## Control Lot Fields

- lot ID
- control name
- manufacturer
- lot number
- assigned mean
- assigned SD
- expiry date

## Boundary Rules

- Any reagent or control lot change is an auditable event
- LJ charts must show a visual lot boundary marker
- Westgard consecutive histories reset on lot boundary by default

## CRUD Expectations

- Create and list reagent lots
- Create and list control lots
- Mark inactive or expired lots
- Reject duplicate active lot number conflicts for the same assay/control scope

## Acceptance Criteria

- Lot registries are queryable and export-safe
- Boundary markers are available to the UI without recomputation
- Lot changes are visible in audit history
