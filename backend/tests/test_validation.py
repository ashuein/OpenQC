"""Unit tests for backend.engine.validation_engine."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

# Ensure the backend package is importable when running pytest from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.engine.validation_engine import (
    calculate_intra_run_precision,
    calculate_inter_run_precision,
    calculate_linearity,
    calculate_lod,
    calculate_loq,
    evaluate_acceptance,
)
from backend.utils.stats import mean, sd


# ---------------------------------------------------------------------------
# LOD
# ---------------------------------------------------------------------------
class TestCalculateLOD:
    def test_known_values(self) -> None:
        blanks = [10.0, 10.5, 9.8, 10.2, 10.1]
        result = calculate_lod(blanks)

        expected_mean = mean(blanks)
        expected_sd = sd(blanks)
        expected_lod = expected_mean + 3 * expected_sd

        assert math.isclose(result["lod"], expected_lod, rel_tol=1e-9)
        assert math.isclose(result["mean"], expected_mean, rel_tol=1e-9)
        assert math.isclose(result["sd"], expected_sd, rel_tol=1e-9)
        assert result["n"] == 5

    def test_fewer_than_2_values_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 2"):
            calculate_lod([5.0])

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 2"):
            calculate_lod([])


# ---------------------------------------------------------------------------
# LOQ
# ---------------------------------------------------------------------------
class TestCalculateLOQ:
    def test_only_last_meets_threshold(self) -> None:
        """Three concentrations, only the last has CV <= threshold."""
        data = [
            {"concentration": 1.0, "replicates": [10.0, 20.0, 30.0]},  # high CV
            {"concentration": 5.0, "replicates": [9.0, 11.0, 13.0]},  # moderate CV
            {"concentration": 10.0, "replicates": [10.0, 10.1, 9.9]},  # low CV
        ]
        # Use a very tight threshold so only the last concentration passes
        result = calculate_loq(data, cv_threshold=1.0)

        assert result["loq"] == 10.0
        assert result["cv_at_loq"] is not None
        assert result["cv_at_loq"] <= 1.0
        assert len(result["all_concentrations"]) == 3
        assert result["all_concentrations"][0]["meets_threshold"] is False
        assert result["all_concentrations"][1]["meets_threshold"] is False
        assert result["all_concentrations"][2]["meets_threshold"] is True

    def test_none_meet_threshold(self) -> None:
        """No concentration meets the CV threshold."""
        data = [
            {"concentration": 1.0, "replicates": [10.0, 20.0, 30.0]},
            {"concentration": 5.0, "replicates": [9.0, 15.0, 21.0]},
        ]
        result = calculate_loq(data, cv_threshold=0.01)

        assert result["loq"] is None
        assert result["cv_at_loq"] is None

    def test_first_meets_threshold(self) -> None:
        """First concentration already meets threshold."""
        data = [
            {"concentration": 1.0, "replicates": [10.0, 10.0, 10.0]},
            {"concentration": 5.0, "replicates": [50.0, 100.0, 150.0]},
        ]
        result = calculate_loq(data, cv_threshold=5.0)

        assert result["loq"] == 1.0


# ---------------------------------------------------------------------------
# Intra-run precision
# ---------------------------------------------------------------------------
class TestIntraRunPrecision:
    def test_known_replicates(self) -> None:
        replicates = [10.0, 10.5, 9.8, 10.2, 10.1]
        result = calculate_intra_run_precision(replicates)

        expected_mean = mean(replicates)
        expected_sd = sd(replicates)
        expected_cv = (expected_sd / expected_mean) * 100.0

        assert math.isclose(result["cv"], expected_cv, rel_tol=1e-9)
        assert math.isclose(result["mean"], expected_mean, rel_tol=1e-9)
        assert math.isclose(result["sd"], expected_sd, rel_tol=1e-9)
        assert result["n"] == 5

    def test_fewer_than_2_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 2"):
            calculate_intra_run_precision([5.0])


# ---------------------------------------------------------------------------
# Inter-run precision
# ---------------------------------------------------------------------------
class TestInterRunPrecision:
    def test_three_runs_evaluated(self) -> None:
        run_means = [
            {"run_id": "R1", "mean": 10.0, "date": "2026-01-01"},
            {"run_id": "R2", "mean": 10.5, "date": "2026-01-02"},
            {"run_id": "R3", "mean": 9.8, "date": "2026-01-03"},
        ]
        result = calculate_inter_run_precision(run_means)

        assert result["status"] == "evaluated"
        assert result["n_runs"] == 3
        assert result["cv"] > 0

        values = [r["mean"] for r in run_means]
        expected_mean = mean(values)
        assert math.isclose(result["mean"], expected_mean, rel_tol=1e-9)

    def test_two_runs_not_evaluated(self) -> None:
        run_means = [
            {"run_id": "R1", "mean": 10.0, "date": "2026-01-01"},
            {"run_id": "R2", "mean": 10.5, "date": "2026-01-02"},
        ]
        result = calculate_inter_run_precision(run_means)

        assert result["status"] == "not_evaluated"
        assert result["n_runs"] == 2

    def test_one_run_not_evaluated(self) -> None:
        result = calculate_inter_run_precision(
            [{"run_id": "R1", "mean": 10.0, "date": "2026-01-01"}]
        )
        assert result["status"] == "not_evaluated"

    def test_empty_not_evaluated(self) -> None:
        result = calculate_inter_run_precision([])
        assert result["status"] == "not_evaluated"
        assert result["n_runs"] == 0


# ---------------------------------------------------------------------------
# Linearity
# ---------------------------------------------------------------------------
class TestLinearity:
    def test_perfect_line(self) -> None:
        """y = 2x + 1 should give R^2=1, slope=2, intercept=1."""
        levels = [
            {"expected": 1.0, "measured": 3.0},
            {"expected": 2.0, "measured": 5.0},
            {"expected": 3.0, "measured": 7.0},
            {"expected": 4.0, "measured": 9.0},
            {"expected": 5.0, "measured": 11.0},
        ]
        result = calculate_linearity(levels)

        assert math.isclose(result["slope"], 2.0, rel_tol=1e-9)
        assert math.isclose(result["intercept"], 1.0, rel_tol=1e-9)
        assert math.isclose(result["r_squared"], 1.0, rel_tol=1e-9)
        assert result["n_levels"] == 5

    def test_fewer_than_3_levels_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 3"):
            calculate_linearity([
                {"expected": 1.0, "measured": 2.0},
                {"expected": 2.0, "measured": 4.0},
            ])

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 3"):
            calculate_linearity([])


# ---------------------------------------------------------------------------
# Acceptance criteria evaluation
# ---------------------------------------------------------------------------
class TestEvaluateAcceptance:
    def test_all_pass(self) -> None:
        results = {"lod": 50.0, "intra_cv": 3.0, "r_squared": 0.998}
        criteria = {
            "lod": {"threshold": 100.0, "operator": "lte"},
            "intra_cv": {"threshold": 5.0, "operator": "lte"},
            "r_squared": {"threshold": 0.99, "operator": "gte"},
        }
        outcome = evaluate_acceptance(results, criteria)

        assert outcome["overall_status"] == "pass"
        assert outcome["details"]["lod"]["status"] == "pass"
        assert outcome["details"]["intra_cv"]["status"] == "pass"
        assert outcome["details"]["r_squared"]["status"] == "pass"

    def test_one_fail(self) -> None:
        results = {"lod": 150.0, "intra_cv": 3.0}
        criteria = {
            "lod": {"threshold": 100.0, "operator": "lte"},
            "intra_cv": {"threshold": 5.0, "operator": "lte"},
        }
        outcome = evaluate_acceptance(results, criteria)

        assert outcome["overall_status"] == "fail"
        assert outcome["details"]["lod"]["status"] == "fail"
        assert outcome["details"]["intra_cv"]["status"] == "pass"

    def test_gte_pass(self) -> None:
        results = {"r_squared": 0.999}
        criteria = {"r_squared": {"threshold": 0.99, "operator": "gte"}}
        outcome = evaluate_acceptance(results, criteria)
        assert outcome["overall_status"] == "pass"

    def test_gte_fail(self) -> None:
        results = {"r_squared": 0.85}
        criteria = {"r_squared": {"threshold": 0.99, "operator": "gte"}}
        outcome = evaluate_acceptance(results, criteria)
        assert outcome["overall_status"] == "fail"

    def test_missing_metric_fails(self) -> None:
        results = {}
        criteria = {"lod": {"threshold": 100.0, "operator": "lte"}}
        outcome = evaluate_acceptance(results, criteria)
        assert outcome["overall_status"] == "fail"
        assert outcome["details"]["lod"]["status"] == "fail"

    def test_empty_criteria_passes(self) -> None:
        results = {"lod": 50.0}
        criteria = {}
        outcome = evaluate_acceptance(results, criteria)
        assert outcome["overall_status"] == "pass"

    def test_boundary_lte(self) -> None:
        """Value exactly at threshold with lte should pass."""
        results = {"intra_cv": 5.0}
        criteria = {"intra_cv": {"threshold": 5.0, "operator": "lte"}}
        outcome = evaluate_acceptance(results, criteria)
        assert outcome["details"]["intra_cv"]["status"] == "pass"

    def test_boundary_gte(self) -> None:
        """Value exactly at threshold with gte should pass."""
        results = {"r_squared": 0.99}
        criteria = {"r_squared": {"threshold": 0.99, "operator": "gte"}}
        outcome = evaluate_acceptance(results, criteria)
        assert outcome["details"]["r_squared"]["status"] == "pass"
