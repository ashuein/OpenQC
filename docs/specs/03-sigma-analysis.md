# Spec 03: Sigma Analysis

| Field | Value |
|---|---|
| Spec ID | 03 |
| Purpose | Define Sigma calculation inputs, outputs, classification, NMEDx plotting, and QC rule recommendation defaults |
| Primary tasks | `docs/tasks/TASK-03-sigma-analysis.md` |
| Owned modules | `backend/engine/sigma_engine.py`, `backend/models/sigma_schemas.py`, `backend/routers/sigma.py` |
| Allowed secondary specs | `docs/specs/02-qc-westgard.md`, `docs/specs/10-api-and-data-contracts.md` |

## Inputs

- `assay`
- `tea_percent`
- `bias_percent`
- `cv_percent`

All inputs are percentages and must be positive except `bias_percent`, which may be zero.

## Core Formula

`sigma_score = (tea_percent - bias_percent) / cv_percent`

Reject invalid inputs when:

- `cv_percent <= 0`
- `tea_percent <= 0`
- `bias_percent < 0`
- `bias_percent > tea_percent` unless explicitly overridden by user validation

## Classification Bands

| Sigma score | Classification |
|---|---|
| `>= 6.0` | `world_class` |
| `>= 5.0 and < 6.0` | `excellent` |
| `>= 4.0 and < 5.0` | `good` |
| `>= 3.0 and < 4.0` | `marginal` |
| `< 3.0` | `unacceptable` |

## NMEDx Coordinates

Use normalized coordinates:

- `nmedx_x = bias_percent / tea_percent`
- `nmedx_y = cv_percent / tea_percent`

If `tea_percent` is missing or zero, NMEDx coordinates must not be produced.

## Recommended QC Rules

Default recommendation map:

| Sigma band | Recommendation |
|---|---|
| `>= 6.0` | low-intensity QC, `1-3s` minimum |
| `5.0 to < 6.0` | `1-3s`, `2-2s`, `R-4s` |
| `4.0 to < 5.0` | full multirule set for routine monitoring |
| `3.0 to < 4.0` | intensified QC and shorter review interval |
| `< 3.0` | method unacceptable until corrected |

The mapping is a documented default, not a substitute for lab policy.

## Outputs

- `assay`
- `sigma_score`
- `classification`
- `recommended_rules`
- `nmedx_x`
- `nmedx_y`

## Acceptance Criteria

- Formula is deterministic and unit-tested.
- Output classifications are stable on band boundaries.
- NMEDx coordinates use normalized TEa values.
- Recommendation text is data-derived, not hardcoded in the UI.
