"""Unit tests for backend.engine.sigma_engine."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

# Ensure the backend package is importable when running pytest from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.engine.sigma_engine import (
    calculate_batch,
    calculate_sigma,
    classify_sigma,
    get_recommended_rules,
)


# ---------------------------------------------------------------------------
# Core formula
# ---------------------------------------------------------------------------
class TestCalculateSigma:
    def test_basic_formula(self) -> None:
        """TEa=10, bias=2, CV=2 -> sigma = 4.0 -> 'good'."""
        result = calculate_sigma(tea_percent=10.0, bias_percent=2.0, cv_percent=2.0)
        assert result["sigma_score"] == 4.0
        assert result["classification"] == "good"

    def test_nmedx_coordinates(self) -> None:
        """TEa=10, bias=3, CV=2 -> nmedx_x=0.3, nmedx_y=0.2."""
        result = calculate_sigma(tea_percent=10.0, bias_percent=3.0, cv_percent=2.0)
        assert math.isclose(result["nmedx_x"], 0.3, rel_tol=1e-9)
        assert math.isclose(result["nmedx_y"], 0.2, rel_tol=1e-9)

    def test_result_keys(self) -> None:
        result = calculate_sigma(tea_percent=10.0, bias_percent=1.0, cv_percent=1.0)
        expected_keys = {"sigma_score", "classification", "recommended_rules", "nmedx_x", "nmedx_y", "notes"}
        assert set(result.keys()) == expected_keys


# ---------------------------------------------------------------------------
# Classification boundaries
# ---------------------------------------------------------------------------
class TestClassifySigma:
    def test_world_class_boundary(self) -> None:
        """sigma = 6.0 exactly -> 'world_class'."""
        assert classify_sigma(6.0) == "world_class"

    def test_world_class_above(self) -> None:
        assert classify_sigma(7.5) == "world_class"

    def test_excellent_boundary(self) -> None:
        """sigma = 5.0 exactly -> 'excellent'."""
        assert classify_sigma(5.0) == "excellent"

    def test_excellent_mid(self) -> None:
        assert classify_sigma(5.5) == "excellent"

    def test_good_boundary(self) -> None:
        """sigma = 4.0 exactly -> 'good'."""
        assert classify_sigma(4.0) == "good"

    def test_good_mid(self) -> None:
        assert classify_sigma(4.5) == "good"

    def test_marginal_boundary(self) -> None:
        """sigma = 3.0 exactly -> 'marginal'."""
        assert classify_sigma(3.0) == "marginal"

    def test_marginal_mid(self) -> None:
        assert classify_sigma(3.5) == "marginal"

    def test_unacceptable(self) -> None:
        """sigma = 2.5 -> 'unacceptable'."""
        assert classify_sigma(2.5) == "unacceptable"

    def test_unacceptable_negative(self) -> None:
        assert classify_sigma(-1.0) == "unacceptable"


# ---------------------------------------------------------------------------
# Recommended rules
# ---------------------------------------------------------------------------
class TestGetRecommendedRules:
    def test_world_class_rules(self) -> None:
        rules, notes = get_recommended_rules(6.0)
        assert rules == ["1-3s"]
        assert notes is None

    def test_excellent_rules(self) -> None:
        rules, notes = get_recommended_rules(5.5)
        assert rules == ["1-3s", "2-2s", "R-4s"]
        assert notes is None

    def test_good_rules(self) -> None:
        rules, notes = get_recommended_rules(4.5)
        assert rules == ["1-3s", "2-2s", "R-4s", "4-1s", "10x"]
        assert notes is None

    def test_marginal_rules(self) -> None:
        rules, notes = get_recommended_rules(3.5)
        assert rules == ["1-3s", "2-2s", "R-4s", "4-1s", "10x"]
        assert notes is not None
        assert "Intensified QC" in notes

    def test_unacceptable_rules(self) -> None:
        rules, notes = get_recommended_rules(2.5)
        assert rules == []
        assert notes is not None
        assert "unacceptable" in notes.lower()


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------
class TestValidation:
    def test_cv_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="cv_percent must be > 0"):
            calculate_sigma(tea_percent=10.0, bias_percent=2.0, cv_percent=0.0)

    def test_cv_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="cv_percent must be > 0"):
            calculate_sigma(tea_percent=10.0, bias_percent=2.0, cv_percent=-1.0)

    def test_tea_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="tea_percent must be > 0"):
            calculate_sigma(tea_percent=-1.0, bias_percent=2.0, cv_percent=2.0)

    def test_tea_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="tea_percent must be > 0"):
            calculate_sigma(tea_percent=0.0, bias_percent=0.0, cv_percent=2.0)

    def test_bias_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="bias_percent must be >= 0"):
            calculate_sigma(tea_percent=10.0, bias_percent=-1.0, cv_percent=2.0)


# ---------------------------------------------------------------------------
# Batch calculation
# ---------------------------------------------------------------------------
class TestCalculateBatch:
    def test_batch_multiple_assays(self) -> None:
        inputs = [
            {"assay": "Glucose", "tea_percent": 10.0, "bias_percent": 2.0, "cv_percent": 2.0},
            {"assay": "HbA1c", "tea_percent": 6.0, "bias_percent": 1.0, "cv_percent": 1.0},
            {"assay": "Sodium", "tea_percent": 4.0, "bias_percent": 1.0, "cv_percent": 2.0},
        ]
        results = calculate_batch(inputs)

        assert len(results) == 3

        # Glucose: (10-2)/2 = 4.0 -> good
        assert results[0]["assay"] == "Glucose"
        assert results[0]["sigma_score"] == 4.0
        assert results[0]["classification"] == "good"

        # HbA1c: (6-1)/1 = 5.0 -> excellent
        assert results[1]["assay"] == "HbA1c"
        assert results[1]["sigma_score"] == 5.0
        assert results[1]["classification"] == "excellent"

        # Sodium: (4-1)/2 = 1.5 -> unacceptable
        assert results[2]["assay"] == "Sodium"
        assert results[2]["sigma_score"] == 1.5
        assert results[2]["classification"] == "unacceptable"

    def test_batch_empty_list(self) -> None:
        results = calculate_batch([])
        assert results == []

    def test_batch_single_assay(self) -> None:
        inputs = [{"assay": "Creatinine", "tea_percent": 15.0, "bias_percent": 3.0, "cv_percent": 2.0}]
        results = calculate_batch(inputs)
        assert len(results) == 1
        # (15-3)/2 = 6.0 -> world_class
        assert results[0]["sigma_score"] == 6.0
        assert results[0]["classification"] == "world_class"
        assert results[0]["assay"] == "Creatinine"
