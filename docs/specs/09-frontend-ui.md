# Spec 09: Frontend UI

| Field | Value |
|---|---|
| Spec ID | 09 |
| Purpose | Define all user-facing screens, layout rules, visual tokens, component policy, Figma workflow, and performance constraints |
| Primary tasks | `docs/tasks/TASK-09-frontend-design-system-and-shell.md`, `docs/tasks/TASK-10-qc-and-dashboard-ui.md`, `docs/tasks/TASK-11-sigma-and-validation-ui.md`, `docs/tasks/TASK-12-audit-lots-rag-ui.md` |
| Owned modules | App shell, views, page headers, navigation, screen-level layout, visual tokens, Figma approval workflow |
| Allowed secondary specs | `docs/specs/10-api-and-data-contracts.md`, `docs/ARCHITECTURE.md` |

## Design Intent

The OpenQC UI must feel clinical, restrained, and fast. It is not a marketing site and must not resemble a gradient-heavy startup dashboard. Information density is acceptable when the layout remains readable and hierarchy is deliberate.

## Screen Inventory

### Dashboard

- recent QC runs
- violation summary
- quick Sigma status
- recent audit activity

### QC Monitor

- upload area
- assay/channel selectors
- LJ chart zone
- violation table
- run summary panel

### Sigma

- TEa/bias/CV inputs
- Sigma results table
- NMEDx chart
- recommendation summary

### Validator

- dataset upload
- acceptance criteria editor
- results table
- linearity chart

### Audit

- audit table
- verification status strip
- export actions

### Lot Registry

- reagent lot table
- control lot table
- inline add/edit forms

### Regulatory Assistant

- question input
- answer card
- source chips
- ingestion status

## App Shell Rules

- Dark left sidebar, light-on-dark typography, no decorative gradients
- Content area uses layered neutral surfaces rather than floating card stacks
- Each page has a persistent page header with title, scope controls, and export action when applicable
- Tables and charts live in dedicated zones with clear separators, not ornamental cards
- Sidebar is the primary global navigation; tabs are for page-local switching only

## State Design

- Loading: use skeletons or reserved layout placeholders, not spinner-only screens
- Empty: show one plain-language explanation and one clear next action
- Error: show impact, recovery action, and preserve entered filters where possible
- Warning: use warning color plus label text
- Pass/Fail: use status badge with text, never color alone
- Row selection: use `section-selected` background, not colored borders or glow

## Tab Behavior

- Active tab uses `tab-active-bg` with `tab-active-text`
- Inactive tab uses transparent background with `tab-inactive-text`
- Tab sets are compact and horizontal
- Tabs are never the only indicator of current section; page context must also be visible

## Figma-First Workflow

- Every major screen must have an approved Figma layout before implementation
- Figma is the visual approval artifact, not an optional reference
- The implementation must follow approved spacing, hierarchy, and token usage
- Any major design change must update the Figma artifact before code changes land
- Frontend task packets must record the relevant Figma frame ID or approved design artifact

## `shadcn-vue` Policy

- Stay on `Vue 3 + Vite`
- Use `shadcn-vue`-style primitives or an equivalent Vue-compatible pattern
- Install only the components required by the approved screen designs
- Prefer composing existing primitives over writing custom wrapper systems
- No large UI kits, template dumps, or unused component packs
- Use semantic tokens and variants, not raw arbitrary color styling

## Visual Token System

| Token | Value |
|---|---|
| `bg-app` | `#0B0D10` |
| `bg-surface` | `#12161B` |
| `bg-surface-2` | `#171C22` |
| `bg-highlight` | `#1E242C` |
| `border-subtle` | `#262D36` |
| `border-strong` | `#343D48` |
| `text-primary` | `#F3F4F6` |
| `text-secondary` | `#B6BDC7` |
| `text-muted` | `#8E97A3` |
| `tab-active-bg` | `#F3F4F6` |
| `tab-active-text` | `#0B0D10` |
| `tab-inactive-bg` | `transparent` |
| `tab-inactive-text` | `#8E97A3` |
| `section-selected` | `#1A2028` |
| `success` | `#43A047` |
| `warning` | `#F9A825` |
| `danger` | `#E53935` |

## Hard Visual Rules

- Grayscale is the base system
- Semantic colors appear only for QC meaning and status
- No purple, blue-violet, or rainbow accent system
- No decorative gradient backgrounds
- No dashboard-card mosaic as the default layout
- No ornamental shadows as the primary hierarchy device
- Charts and tables carry content; layout carries structure

## Performance Rules

- Use route-level lazy loading
- Load chart libraries only on screens that need them
- Avoid global animation libraries unless approved in spec
- Keep dependency additions explicit and justified
- Prefer CSS and layout discipline over effect-heavy UI

## Acceptance Criteria

- This spec is the sole owner of UI tokens, tab styles, highlight rules, and Figma policy
- All frontend tasks can be implemented from this spec plus API contracts
- Screen designs remain monotone, restrained, and legible
