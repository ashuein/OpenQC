# Spec 07: Reporting

| Field | Value |
|---|---|
| Spec ID | 07 |
| Purpose | Define report composition for QC, validation, Sigma, and audit outputs |
| Primary tasks | `docs/tasks/TASK-07-reporting.md` |
| Owned modules | `backend/engine/report_engine.py`, PDF templates, export endpoints |
| Allowed secondary specs | `docs/specs/02-qc-westgard.md`, `docs/specs/03-sigma-analysis.md`, `docs/specs/04-assay-validation.md`, `docs/specs/05-audit-trail.md` |

## Report Types

- QC run report PDF
- Validation report PDF
- Sigma report PDF
- Audit export JSON and PDF

## Composition Rules

- Reporting consumes already-calculated domain outputs
- Templates are HTML-first and rendered to PDF through WeasyPrint
- Charts are embedded as images or serialized chart exports, not recalculated in the template

## Required Sections

### QC report

- run metadata
- control lot and reagent lot
- LJ chart
- violation list
- summary stats

### Validation report

- assay metadata
- raw table summary
- metrics table
- acceptance thresholds
- pass/fail summary

### Sigma report

- assay list
- sigma table
- classification
- NMEDx chart
- recommended rules

### Audit report

- verification status
- event chronology
- chain integrity metadata

## Acceptance Criteria

- Every report is reproducible from stored module outputs
- PDF generation does not mutate domain data
- Audit export contains enough data for independent verification
