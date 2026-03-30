# OpenQC AI Routing Guide

This file is the single entrypoint for any AI agent working in this repository.

## Read Protocol

1. Identify the work type.
2. Read exactly one primary spec first.
3. Read a secondary spec only if the primary spec explicitly allows it.
4. Read [ARCHITECTURE.md](ARCHITECTURE.md) only for boundary-spanning or whole-system questions.
5. Do not read unrelated specs by default.

## Primary Routing Table

| Work type | Primary spec | Allowed secondary specs | Notes |
|---|---|---|---|
| App shell, layout, tabs, page headers, tables, empty states, loading states, theme, tokens, accessibility visuals, `shadcn-vue` policy | `docs/specs/09-frontend-ui.md` | `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md` | Frontend UI spec owns user-facing design and interaction rules |
| QC engine, Westgard rules, violation detection, run status, control ordering, lot resets | `docs/specs/02-qc-westgard.md` | `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md` | Westgard spec is the only source of truth for rule behavior |
| Sigma math, NMEDx, QC rule recommendations | `docs/specs/03-sigma-analysis.md` | `docs/specs/02-qc-westgard.md`, `docs/specs/10-api-and-data-contracts.md` | Sigma spec owns formulas and output classification |
| LOD, LOQ, intra/inter-run precision, linearity | `docs/specs/04-assay-validation.md` | `docs/specs/10-api-and-data-contracts.md` | Validation spec owns assay calculations |
| Hashing, audit chain, tamper checks, event logging | `docs/specs/05-audit-trail.md` | `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md` | Audit spec owns chain integrity rules |
| Reagent lots, control lots, boundary markers | `docs/specs/06-lot-tracker.md` | `docs/specs/02-qc-westgard.md`, `docs/specs/10-api-and-data-contracts.md` | Lot behavior resets QC history unless stated otherwise |
| PDF exports, JSON audit export, report sections | `docs/specs/07-reporting.md` | `docs/specs/02-qc-westgard.md`, `docs/specs/03-sigma-analysis.md`, `docs/specs/04-assay-validation.md`, `docs/specs/05-audit-trail.md` | Reporting spec owns output composition |
| Regulatory corpus ingestion, retrieval, reranking, answer formatting | `docs/specs/08-regulatory-rag.md` | `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md` | RAG spec owns assistant behavior |
| Endpoint shapes, payload schemas, errors, IDs, exports, timestamps | `docs/specs/10-api-and-data-contracts.md` | `docs/ARCHITECTURE.md` | Contract spec owns canonical wire shapes |
| Module boundaries, end-to-end flow, dependency questions | `docs/ARCHITECTURE.md` | Any directly involved primary spec | Architecture is for cross-cutting work only |

## Keyword Routing

| Keywords | Primary spec |
|---|---|
| `sidebar`, `header`, `tabs`, `badge`, `chart zone`, `color token`, `highlight`, `loading skeleton`, `empty state`, `figma`, `shadcn-vue` | `docs/specs/09-frontend-ui.md` |
| `1-2s`, `1-3s`, `2-2s`, `R-4s`, `4-1s`, `10x`, `reject`, `warning`, `consecutive`, `lot reset` | `docs/specs/02-qc-westgard.md` |
| `sigma`, `TEa`, `bias`, `CV`, `NMEDx`, `classification` | `docs/specs/03-sigma-analysis.md` |
| `LOD`, `LOQ`, `precision`, `linearity`, `R²`, `acceptance criteria` | `docs/specs/04-assay-validation.md` |
| `hash`, `tamper`, `audit`, `chain`, `verify`, `event log` | `docs/specs/05-audit-trail.md` |
| `reagent lot`, `control lot`, `expiry`, `lot marker` | `docs/specs/06-lot-tracker.md` |
| `pdf`, `export`, `report`, `weasyprint`, `template` | `docs/specs/07-reporting.md` |
| `ingest`, `chunk`, `embed`, `retrieve`, `rerank`, `source citation` | `docs/specs/08-regulatory-rag.md` |
| `request`, `response`, `schema`, `pagination`, `content-type`, `uuid` | `docs/specs/10-api-and-data-contracts.md` |

## Task-to-Spec Map

| Task file | Primary spec |
|---|---|
| `docs/tasks/TASK-01-backend-core.md` | `docs/specs/01-backend-core.md` |
| `docs/tasks/TASK-02-qc-westgard.md` | `docs/specs/02-qc-westgard.md` |
| `docs/tasks/TASK-03-sigma-analysis.md` | `docs/specs/03-sigma-analysis.md` |
| `docs/tasks/TASK-04-assay-validation.md` | `docs/specs/04-assay-validation.md` |
| `docs/tasks/TASK-05-audit-trail.md` | `docs/specs/05-audit-trail.md` |
| `docs/tasks/TASK-06-lot-tracker.md` | `docs/specs/06-lot-tracker.md` |
| `docs/tasks/TASK-07-reporting.md` | `docs/specs/07-reporting.md` |
| `docs/tasks/TASK-08-regulatory-rag.md` | `docs/specs/08-regulatory-rag.md` |
| `docs/tasks/TASK-09-frontend-design-system-and-shell.md` | `docs/specs/09-frontend-ui.md` |
| `docs/tasks/TASK-10-qc-and-dashboard-ui.md` | `docs/specs/09-frontend-ui.md` |
| `docs/tasks/TASK-11-sigma-and-validation-ui.md` | `docs/specs/09-frontend-ui.md` |
| `docs/tasks/TASK-12-audit-lots-rag-ui.md` | `docs/specs/09-frontend-ui.md` |
| `docs/tasks/TASK-13-integration-and-sample-data.md` | `docs/ARCHITECTURE.md` |
| `docs/tasks/TASK-14-readme-and-release-prep.md` | `docs/ARCHITECTURE.md` |

## Escalation Rules

- Escalate to `docs/specs/10-api-and-data-contracts.md` when a screen or engine task changes request or response shapes.
- Escalate to `docs/ARCHITECTURE.md` when a change touches more than one subsystem boundary.
- Do not redefine UI tokens outside `docs/specs/09-frontend-ui.md`.
- Do not redefine Westgard behavior outside `docs/specs/02-qc-westgard.md`.
