"""
OpenQC API -- FastAPI application entry point.

Configures CORS, registers all module routers, and exposes a root
health-check endpoint.  No business logic lives here.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db.database import init_db
from backend.routers import audit, lots, qc, rag, settings, sigma, validation


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: initialise the database on startup."""
    init_db()
    yield


app = FastAPI(
    title="OpenQC API",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS -- allow the Vite dev server during local development
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(qc.router)
app.include_router(sigma.router)
app.include_router(validation.router)
app.include_router(audit.router)
app.include_router(lots.router)
app.include_router(rag.router)
app.include_router(settings.router)


# ---------------------------------------------------------------------------
# Root health check
# ---------------------------------------------------------------------------
@app.get("/")
def root() -> dict:
    """Simple health-check endpoint."""
    return {"status": "ok", "app": "OpenQC"}
