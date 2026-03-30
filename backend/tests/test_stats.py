"""Unit tests for backend.utils.stats."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

# Ensure the backend package is importable when running pytest from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.utils.stats import cv, linear_regression, mean, sd, z_score


# ---------------------------------------------------------------------------
# mean
# ---------------------------------------------------------------------------
class TestMean:
    def test_normal_list(self) -> None:
        assert mean([1.0, 2.0, 3.0, 4.0, 5.0]) == 3.0

    def test_single_value(self) -> None:
        assert mean([42.0]) == 42.0

    def test_empty_list_raises(self) -> None:
        with pytest.raises(ValueError, match="at least one value"):
            mean([])


# ---------------------------------------------------------------------------
# sd
# ---------------------------------------------------------------------------
class TestSd:
    def test_normal_list(self) -> None:
        # sd([1, 2, 3, 4, 5], ddof=1) = sqrt(10/4) = sqrt(2.5)
        result = sd([1.0, 2.0, 3.0, 4.0, 5.0])
        assert math.isclose(result, math.sqrt(2.5), rel_tol=1e-9)

    def test_single_value_ddof1_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 2 values"):
            sd([5.0], ddof=1)

    def test_single_value_ddof0(self) -> None:
        # Population SD of a single value is 0.
        assert sd([5.0], ddof=0) == 0.0

    def test_empty_list_raises(self) -> None:
        with pytest.raises(ValueError, match="at least one value"):
            sd([])


# ---------------------------------------------------------------------------
# cv
# ---------------------------------------------------------------------------
class TestCv:
    def test_normal_list(self) -> None:
        values = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        expected = (sd(values) / mean(values)) * 100.0
        assert math.isclose(cv(values), expected, rel_tol=1e-9)

    def test_zero_mean_returns_inf(self) -> None:
        # Mean of [-1, 1] is 0 -> inf
        assert cv([-1.0, 1.0]) == float("inf")


# ---------------------------------------------------------------------------
# z_score
# ---------------------------------------------------------------------------
class TestZScore:
    def test_normal(self) -> None:
        assert z_score(10.0, 5.0, 2.5) == 2.0

    def test_zero_sd_raises(self) -> None:
        with pytest.raises(ValueError, match="non-zero standard deviation"):
            z_score(10.0, 5.0, 0.0)


# ---------------------------------------------------------------------------
# linear_regression
# ---------------------------------------------------------------------------
class TestLinearRegression:
    def test_perfect_line(self) -> None:
        # y = 2x + 1
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [3.0, 5.0, 7.0, 9.0, 11.0]
        result = linear_regression(x, y)
        assert math.isclose(result["slope"], 2.0, rel_tol=1e-9)
        assert math.isclose(result["intercept"], 1.0, rel_tol=1e-9)
        assert math.isclose(result["r_squared"], 1.0, rel_tol=1e-9)

    def test_fewer_than_two_points_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 2"):
            linear_regression([1.0], [2.0])

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 2"):
            linear_regression([], [])

    def test_mismatched_lengths_raises(self) -> None:
        with pytest.raises(ValueError, match="same length"):
            linear_regression([1.0, 2.0], [1.0])
