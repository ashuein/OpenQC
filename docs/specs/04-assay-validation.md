# Spec 04: Assay Validation

| Field | Value |
|---|---|
| Spec ID | 04 |
| Purpose | Define validation dataset handling and formulas for LOD, LOQ, precision, and linearity |
| Primary tasks | `docs/tasks/TASK-04-assay-validation.md` |
| Owned modules | `backend/engine/validation_engine.py`, `backend/models/validation_schemas.py`, `backend/routers/validation.py` |
| Allowed secondary specs | `docs/specs/10-api-and-data-contracts.md` |

## Validation Modes

- LOD
- LOQ
- Intra-run precision
- Inter-run precision
- Linearity

## Canonical Dataset Requirements

Every validation dataset must capture:

- assay identifier
- run identifier
- concentration or dilution level where applicable
- replicate index
- measured value
- capture date

## Formula Rules

- LOD default: `mean(blank_or_lowest_replicates) + 3 * SD(blank_or_lowest_replicates)`
- LOQ default: lowest concentration with `CV <= user_defined_threshold`
- Intra-run precision: `CV` across replicates within one run
- Inter-run precision: `CV` across at least three runs over at least three dates when available
- Linearity: simple linear regression with slope and `R²`

## Acceptance Logic

- Acceptance thresholds are user-configurable and stored with the validation run
- Each measured parameter returns `pass | fail`
- Overall validation status is `fail` if any required parameter fails

## Outputs

- raw input summary
- calculated metrics
- acceptance thresholds used
- pass/fail flags per metric
- overall validation status

## Edge Cases

- Reject datasets missing replicate structure
- Reject linearity runs with fewer than three levels
- Mark inter-run precision as `not_evaluated` if minimum run count is not met

## Acceptance Criteria

- Calculations are deterministic from raw datasets
- User-defined thresholds are preserved in output and reports
- Validation report inputs are complete enough for PDF export without recomputation
