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
