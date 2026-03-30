# Task 10: QC and Dashboard UI

- Goal: implement Dashboard and QC Monitor screens from approved Figma frames
- Primary spec: `docs/specs/09-frontend-ui.md`
- Allowed secondary specs: `docs/specs/10-api-and-data-contracts.md`
- Owned modules: `DashboardView`, `QCMonitorView`, QC-related shared components
- Inputs: approved Figma frame IDs, QC API contracts
- Deliverables: dashboard layout, QC upload flow, LJ chart zone, violation table, run summary
- Dependencies: Task 09, Task 02
- Acceptance tests: active/inactive tab styling follows tokens, chart and table zones follow layout rules, empty/loading/error states are implemented, no screen-specific bloat is introduced
- Done definition: dashboard and QC monitor are production-shaped and contract-aligned
- Out of scope: Sigma, validation, audit, and RAG screens
