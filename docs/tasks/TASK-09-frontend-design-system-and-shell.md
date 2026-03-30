# Task 09: Frontend Design System and Shell

- Goal: define and implement the app shell, visual token system, approved component inventory, and Figma-approved structural layouts
- Primary spec: `docs/specs/09-frontend-ui.md`
- Allowed secondary specs: `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md`
- Owned modules: app shell, sidebar, page header, shared tokens, shared status components
- Inputs: approved Figma shell artifact, frontend UI spec
- Deliverables: shell layout, tokenized CSS variables, approved `shadcn-vue` primitive inventory, shared loading/empty/error states
- Dependencies: none on backend implementation, but API contract awareness required
- Acceptance tests: shell matches approved Figma, tokens are centralized, no purple or gradients appear, shared states are reusable
- Done definition: all screen tasks can build on a stable shell and token system
- Out of scope: module-specific charts and tables
