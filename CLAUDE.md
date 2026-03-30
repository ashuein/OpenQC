# OpenQC -- AI Agent Guide

Start with `docs/AI-ROUTING.md` for the routing table.

## Quick Reference

- Backend runs from project root: `uvicorn backend.main:app`
- All Python imports use `backend.` prefix
- Frontend at `frontend/`, dev server on port 5173
- Backend API on port 8000
- Tests: `python -m pytest backend/tests/ -v`
- Frontend build: `cd frontend && npm run build`

## Key Rules

- Engine modules (`backend/engine/`) are pure logic -- no I/O, no DB
- Parsers return canonical structures, never UI objects
- Repositories own CRUD, engines own calculations
- Frontend uses CSS custom properties for all colors (see `frontend/src/assets/styles/main.css`)
- API contracts defined in `docs/specs/10-api-and-data-contracts.md`
- Westgard rule behavior defined only in `docs/specs/02-qc-westgard.md`
- UI tokens defined only in `docs/specs/09-frontend-ui.md`

## Post-Refactor Review Gate

After completing any refactoring, bug fix batch, or feature implementation, run a Codex review before considering the work done. This is mandatory — do not skip it.

### Steps

1. Stage and commit changes:
   ```bash
   cd D:/SOFTWARE_Projects_LP/OpenQC
   git add -A && git commit -m "<describe changes>"
   ```

2. Run Codex review against the commit:
   ```bash
   codex review --commit HEAD
   ```

3. Read the review output (may be large — the findings are at the end of the output).

4. Fix every finding you agree with. If you disagree with a finding, state why explicitly.

5. After fixing, commit again and re-run `codex review --commit HEAD`.

6. Repeat until the review is clean or you have explicitly justified every remaining finding. Minimum 5 iterations if findings keep appearing.
