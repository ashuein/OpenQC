# Spec 02: QC and Westgard Rules

| Field | Value |
|---|---|
| Spec ID | 02 |
| Purpose | Define canonical QC run structures, Westgard rule evaluation semantics, applicability, outputs, and test vectors |
| Primary tasks | `docs/tasks/TASK-02-qc-westgard.md` |
| Owned modules | `backend/routers/qc.py`, `backend/engine/westgard_rules.py`, `backend/models/qc_schemas.py`, `backend/db/qc_repository.py` |
| Allowed secondary specs | `docs/specs/06-lot-tracker.md`, `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md` |

## Purpose

This document is the only source of truth for QC run analysis and Westgard rule behavior. No other spec or code path may redefine rule logic.

## Canonical QC Ordering

Every QC point must be evaluated in a deterministic sequence defined by:

1. assay
2. channel
3. control level
4. reagent lot
5. control lot
6. run timestamp
7. within-run sequence index

Multi-point rules only compare points inside the same evaluation stream. A stream is the ordered set of QC points sharing the first five keys above.

## Assay Configuration Model

Each assay profile must declare:

- `controls_per_run`
- `control_levels_supported`
- `r4s_enabled`
- `cross_run_multirule_enabled`
- `lot_reset_required` default `true`

Defaults:

- Single-control assays: `r4s_enabled = false`
- Multi-control assays with at least two eligible control results per run: `r4s_enabled = true`
- `cross_run_multirule_enabled = true`
- `lot_reset_required = true`

## Rule Applicability Matrix

| Rule | Requires | Applies to single-control assays | Applies to multi-control assays |
|---|---|---|---|
| `1-2s` | one point with mean and SD | yes | yes |
| `1-3s` | one point with mean and SD | yes | yes |
| `2-2s` | two consecutive eligible points on same side beyond 2 SD | yes, across runs | yes |
| `R-4s` | two eligible points in the same run, one above +2 SD and one below -2 SD | no | yes |
| `4-1s` | four consecutive eligible points on same side beyond 1 SD | yes, across runs | yes |
| `10x` | ten consecutive eligible points on same side of the mean | yes, across runs | yes |

## Threshold Semantics

- `1-2s` triggers only when `abs(z_score) > 2.0`
- `1-3s` triggers only when `abs(z_score) > 3.0`
- `2-2s` triggers only when both consecutive points satisfy `z_score > 2.0` or both satisfy `z_score < -2.0`
- `R-4s` triggers only when one eligible point in the same run satisfies `z_score > 2.0` and another satisfies `z_score < -2.0`, with total spread strictly greater than `4.0 SD`
- `4-1s` triggers only when four consecutive points satisfy `z_score > 1.0` or all satisfy `z_score < -1.0`
- `10x` triggers only when ten consecutive points remain strictly above the mean or strictly below the mean
- Exact equality at `2 SD`, `3 SD`, or `1 SD` does not trigger the rule

## Evaluation Order

Rules are checked in this order:

1. `1-2s`
2. `1-3s`
3. `2-2s`
4. `R-4s`
5. `4-1s`
6. `10x`

Evaluation continues after a reject rule so the system can capture a complete violation log. The first reject-level rule is stored separately as the run disposition trigger.

## Warning vs Reject

| Rule | Severity | Effect on run status |
|---|---|---|
| `1-2s` | warning | status remains warning unless a reject rule also fires |
| `1-3s`, `2-2s`, `R-4s`, `4-1s`, `10x` | reject | run status becomes reject |

Run status precedence:

`reject > warning > pass`

## Lot Boundary Reset

- If reagent lot changes, consecutive histories for `2-2s`, `4-1s`, and `10x` reset.
- If control lot changes, consecutive histories for `2-2s`, `4-1s`, and `10x` reset.
- `R-4s` never bridges runs and is unaffected by prior run history.
- A hard lot reset is the default and must be reflected in charts and logs.

## Missing or Sparse History

- If there are not enough prior eligible points for a rule window, the rule returns `not_evaluated`.
- Missing runs do not invalidate history, but missing QC points inside an expected sequence do.
- Manually deleted or voided points break consecutive chains.

## Output Contract

Each analyzed run must produce:

- `run_status`: `pass | warning | reject`
- `first_reject_rule`: first reject-level rule in evaluation order or `null`
- `violations`: ordered list of all triggered rules
- `warning_rules`: subset containing warnings
- `reject_rules`: subset containing reject-level rules
- `evaluated_points`: QC points with z-scores and triggered rule codes
- `history_window_used`: point IDs referenced for each multi-point decision

## Golden Test Sequences

These sequences are canonical unit-test vectors. `μ = mean`, `σ = SD`.

### `1-2s`

- Pass: `μ + 1.99σ`
- Warning: `μ + 2.01σ`

### `1-3s`

- Pass: `μ - 2.99σ`
- Reject: `μ - 3.01σ`

### `2-2s`

- Pass: `[μ + 2.10σ, μ + 1.90σ]`
- Reject: `[μ + 2.10σ, μ + 2.20σ]`

### `R-4s`

- Pass: same run points `[μ + 2.10σ, μ - 1.80σ]`
- Reject: same run points `[μ + 2.10σ, μ - 2.10σ]`

### `4-1s`

- Pass: `[μ + 1.10σ, μ + 1.20σ, μ + 0.95σ, μ + 1.30σ]`
- Reject: `[μ + 1.10σ, μ + 1.20σ, μ + 1.05σ, μ + 1.30σ]`

### `10x`

- Pass: nine consecutive points above the mean
- Reject: ten consecutive points above the mean

## References

- Westgard multirule QC lessons and rule explanations
- Westgard Sigma rule selection guidance
- Internal lab SOP or validation policy, if stricter than this spec

## Acceptance Criteria

- Single-control assays cannot trigger `R-4s`.
- Multi-point rules respect ordering and lot reset behavior.
- Full violation capture is recorded even when run status is already reject.
- Unit tests cover pass, warning, reject, boundary, sparse-history, and lot-reset cases.
