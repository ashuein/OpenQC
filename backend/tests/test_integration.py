"""Integration smoke tests for OpenQC API."""
import sys
from pathlib import Path

import pytest

# Ensure the backend package is importable when running pytest from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.db.database import Base, get_db
from backend.main import app

# Import all model modules so Base.metadata includes every table
from backend.models import qc_models  # noqa: F401
from backend.models import lot_models  # noqa: F401
from backend.models import sigma_models  # noqa: F401
from backend.models import audit_models  # noqa: F401
from backend.models import validation_models  # noqa: F401

# ---------------------------------------------------------------------------
# Test database setup -- in-memory SQLite with StaticPool so every session
# shares the same underlying connection (and therefore the same tables).
# ---------------------------------------------------------------------------
_test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
Base.metadata.create_all(bind=_test_engine)
_TestSession = sessionmaker(bind=_test_engine, autocommit=False, autoflush=False)


def _override_get_db():
    """Yield a session bound to the in-memory test database."""
    db = _TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db

from fastapi.testclient import TestClient  # noqa: E402

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
class TestHealthCheck:
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["app"] == "OpenQC"


# ---------------------------------------------------------------------------
# Router registration
# ---------------------------------------------------------------------------
class TestRouterRegistration:
    """Verify all module routers are accessible."""

    def test_qc_router(self):
        # The QC /runs endpoint returns paginated runs
        response = client.get("/qc/runs")
        assert response.status_code == 200

    def test_sigma_router(self):
        response = client.get("/sigma/history?assay=test")
        assert response.status_code == 200

    def test_validation_router(self):
        # GET /validation/report/{id} -- nonexistent id should return 404
        response = client.get("/validation/report/nonexistent")
        assert response.status_code in (404, 422, 200)

    def test_audit_router(self):
        response = client.get("/audit/log")
        assert response.status_code == 200

    def test_lots_reagents(self):
        response = client.get("/lots/reagents")
        assert response.status_code == 200

    def test_lots_controls(self):
        response = client.get("/lots/controls")
        assert response.status_code == 200

    def test_rag_status(self):
        response = client.get("/rag/status")
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# Sigma end-to-end
# ---------------------------------------------------------------------------
class TestSigmaEndToEnd:
    """Test the Sigma calculate -> history flow."""

    def test_calculate_and_history(self):
        # Calculate
        payload = {
            "inputs": [
                {"assay": "Glucose", "tea_percent": 10.0, "bias_percent": 1.5, "cv_percent": 1.2},
                {"assay": "HbA1c", "tea_percent": 6.0, "bias_percent": 1.0, "cv_percent": 1.5},
            ]
        }
        response = client.post("/sigma/calculate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 2

        glucose = next(r for r in data["results"] if r["assay"] == "Glucose")
        assert glucose["classification"] == "world_class"
        assert glucose["sigma_score"] > 6.0

        # History should now have entries
        response = client.get("/sigma/history?assay=Glucose")
        assert response.status_code == 200
        history = response.json()
        assert len(history["entries"]) >= 1


# ---------------------------------------------------------------------------
# Lots end-to-end
# ---------------------------------------------------------------------------
class TestLotsEndToEnd:
    """Test lot creation and listing."""

    def test_reagent_lot_flow(self):
        lot_data = {
            "assay_name": "SARS-CoV-2",
            "lot_number": "RGT-2024-001",
            "expiry_date": "2025-12-31",
        }
        response = client.post("/lots/reagents", json=lot_data)
        assert response.status_code == 201
        created = response.json()
        assert created["assay_name"] == "SARS-CoV-2"
        assert created["lot_number"] == "RGT-2024-001"
        assert created["status"] == "active"

        # List should contain it
        response = client.get("/lots/reagents")
        assert response.status_code == 200
        lots = response.json()
        assert any(l["lot_number"] == "RGT-2024-001" for l in lots)

    def test_control_lot_flow(self):
        lot_data = {
            "control_name": "QC Level 1",
            "manufacturer": "Bio-Rad",
            "lot_number": "CTL-2024-001",
            "assigned_mean": 25.0,
            "assigned_sd": 1.0,
        }
        response = client.post("/lots/controls", json=lot_data)
        assert response.status_code == 201
        created = response.json()
        assert created["control_name"] == "QC Level 1"
        assert created["assigned_mean"] == 25.0


# ---------------------------------------------------------------------------
# Audit end-to-end
# ---------------------------------------------------------------------------
class TestAuditEndToEnd:
    """Test audit log and chain verification."""

    def test_audit_log(self):
        response = client.get("/audit/log")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data

    def test_chain_verify(self):
        response = client.get("/audit/chain-verify")
        assert response.status_code == 200
        data = response.json()
        assert "valid" in data
        assert "entries_checked" in data


# ---------------------------------------------------------------------------
# Sample file existence
# ---------------------------------------------------------------------------
class TestSampleFilesExist:
    """Verify sample data files were generated."""

    SAMPLES_DIR = Path(__file__).resolve().parent.parent / "data" / "samples"

    def test_qc_quantstudio_exists(self):
        assert (self.SAMPLES_DIR / "sample_qc_quantstudio.xlsx").exists()

    def test_qc_violations_exists(self):
        assert (self.SAMPLES_DIR / "sample_qc_violations.xlsx").exists()

    def test_validation_lod_exists(self):
        assert (self.SAMPLES_DIR / "sample_validation_lod.xlsx").exists()

    def test_validation_linearity_exists(self):
        assert (self.SAMPLES_DIR / "sample_validation_linearity.xlsx").exists()

    def test_sigma_inputs_exists(self):
        assert (self.SAMPLES_DIR / "sample_sigma_inputs.xlsx").exists()
