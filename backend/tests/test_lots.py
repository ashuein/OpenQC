"""Unit tests for lot tracking repository functions."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session

# Ensure the backend package is importable when running pytest from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.db.database import Base
from backend.models import lot_models  # noqa: F401  -- register tables on Base
from backend.db.lot_repository import (
    create_control_lot,
    create_reagent_lot,
    list_control_lots,
    list_reagent_lots,
    update_reagent_lot_status,
)

# ---------------------------------------------------------------------------
# Test session setup -- in-memory SQLite
# ---------------------------------------------------------------------------
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(bind=engine)
TestSession = sessionmaker(bind=engine)


@pytest.fixture()
def db():
    """Yield an isolated database session per test.

    Uses a connection-level transaction + nested savepoints so that
    repository functions can call ``session.commit()`` without actually
    persisting data beyond the scope of a single test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSession(bind=connection)

    # Each time the session would commit, start a new savepoint instead
    # so that the outer transaction is never finalised.
    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):
        nonlocal nested
        if trans.nested and not trans._parent.nested:
            nested = connection.begin_nested()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


# ---------------------------------------------------------------------------
# Reagent lot tests
# ---------------------------------------------------------------------------
class TestReagentLots:
    def test_create_reagent_lot(self, db):
        """Create reagent lot -- fields persist correctly."""
        lot = create_reagent_lot(db, {
            "assay_name": "Glucose",
            "lot_number": "R-001",
            "expiry_date": date(2026, 12, 31),
            "open_date": date(2026, 1, 15),
        })
        assert lot.id is not None
        assert lot.assay_name == "Glucose"
        assert lot.lot_number == "R-001"
        assert lot.expiry_date == date(2026, 12, 31)
        assert lot.open_date == date(2026, 1, 15)
        assert lot.status == "active"
        assert lot.created_at is not None

    def test_duplicate_active_reagent_lot_raises(self, db):
        """Duplicate active reagent lot for same assay -> ValueError."""
        create_reagent_lot(db, {"assay_name": "Glucose", "lot_number": "R-001"})
        with pytest.raises(ValueError, match="Active reagent lot"):
            create_reagent_lot(db, {"assay_name": "Glucose", "lot_number": "R-001"})

    def test_same_lot_number_different_assay_ok(self, db):
        """Same lot_number for a different assay is allowed."""
        lot1 = create_reagent_lot(db, {"assay_name": "Glucose", "lot_number": "R-100"})
        lot2 = create_reagent_lot(db, {"assay_name": "HbA1c", "lot_number": "R-100"})
        assert lot1.id != lot2.id

    def test_list_reagent_lots(self, db):
        """List reagent lots returns all entries."""
        create_reagent_lot(db, {"assay_name": "Glucose", "lot_number": "R-200"})
        create_reagent_lot(db, {"assay_name": "Sodium", "lot_number": "R-201"})
        lots = list_reagent_lots(db)
        lot_numbers = {lot.lot_number for lot in lots}
        assert "R-200" in lot_numbers
        assert "R-201" in lot_numbers

    def test_update_reagent_lot_status(self, db):
        """Update lot status to inactive -- status changes."""
        lot = create_reagent_lot(db, {"assay_name": "Potassium", "lot_number": "R-300"})
        updated = update_reagent_lot_status(db, lot.id, "inactive")
        assert updated is not None
        assert updated.status == "inactive"


# ---------------------------------------------------------------------------
# Control lot tests
# ---------------------------------------------------------------------------
class TestControlLots:
    def test_create_control_lot(self, db):
        """Create control lot -- fields persist correctly."""
        lot = create_control_lot(db, {
            "control_name": "Normal Control",
            "manufacturer": "BioRad",
            "lot_number": "C-001",
            "assigned_mean": 5.5,
            "assigned_sd": 0.3,
            "expiry_date": date(2026, 6, 30),
        })
        assert lot.id is not None
        assert lot.control_name == "Normal Control"
        assert lot.manufacturer == "BioRad"
        assert lot.lot_number == "C-001"
        assert lot.assigned_mean == 5.5
        assert lot.assigned_sd == 0.3
        assert lot.expiry_date == date(2026, 6, 30)
        assert lot.status == "active"
        assert lot.created_at is not None

    def test_duplicate_active_control_lot_raises(self, db):
        """Duplicate active control lot for same control -> ValueError."""
        create_control_lot(db, {"control_name": "Normal Control", "lot_number": "C-001"})
        with pytest.raises(ValueError, match="Active control lot"):
            create_control_lot(db, {"control_name": "Normal Control", "lot_number": "C-001"})

    def test_list_control_lots(self, db):
        """List control lots returns all entries."""
        create_control_lot(db, {"control_name": "Normal Control", "lot_number": "C-200"})
        create_control_lot(db, {"control_name": "Abnormal Control", "lot_number": "C-201"})
        lots = list_control_lots(db)
        lot_numbers = {lot.lot_number for lot in lots}
        assert "C-200" in lot_numbers
        assert "C-201" in lot_numbers
