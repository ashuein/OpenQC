"""
Database configuration for OpenQC.

Provides SQLAlchemy engine, session factory, declarative base,
and FastAPI dependency for database session injection.
"""

from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Database file lives inside backend/data/
_DB_DIR = Path(__file__).resolve().parent.parent / "data"
_DB_PATH = _DB_DIR / "openqc.db"
DATABASE_URL = f"sqlite:///{_DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # required for SQLite
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""

    pass


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session and ensures cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables defined by models that inherit from Base.

    Models must be imported before create_all() so their table
    metadata is registered on Base.  Add each new model module
    to the import block below.
    """
    # -- Import all ORM model modules so Base.metadata is populated --
    # Add new model imports here as modules are created:
    from backend.models import qc_models  # noqa: F401
    from backend.models import lot_models  # noqa: F401
    from backend.models import sigma_models  # noqa: F401
    from backend.models import audit_models  # noqa: F401
    from backend.models import validation_models  # noqa: F401

    _DB_DIR.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
