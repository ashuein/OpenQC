"""Golden test vectors for the Westgard multi-rule engine.

All tests use mu=25.0 and sigma=1.0 so that z_score = ct_value - 25.0.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure the backend package is importable when running from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.engine.westgard_rules import (
    check_1_2s,
    check_1_3s,
    check_2_2s,
    check_4_1s,
    check_10x,
    check_r_4s,
    evaluate_rules,
)

MU = 25.0
SD = 1.0


def _pt(ct: float, level: str = "L1", idx: int = 0) -> dict:
    """Convenience: build a point dict."""
    return {
        "ct_value": ct,
        "mean": MU,
        "sd": SD,
        "control_level": level,
        "sequence_index": idx,
    }


# ---------------------------------------------------------------------------
# 1-2s  (warning rule)
# ---------------------------------------------------------------------------
class Test1_2s:
    def test_pass_below_threshold(self) -> None:
        # mu + 1.99*sigma -> z = 1.99 -> no trigger
        assert check_1_2s(1.99) is False

    def test_warning_above_threshold(self) -> None:
        # mu + 2.01*sigma -> z = 2.01 -> trigger
        assert check_1_2s(2.01) is True

    def test_boundary_exact_2_does_not_trigger(self) -> None:
        assert check_1_2s(2.0) is False

    def test_negative_warning(self) -> None:
        assert check_1_2s(-2.01) is True

    def test_negative_exact_does_not_trigger(self) -> None:
        assert check_1_2s(-2.0) is False


# ---------------------------------------------------------------------------
# 1-3s  (reject rule)
# ---------------------------------------------------------------------------
class Test1_3s:
    def test_pass_below_threshold(self) -> None:
        # mu - 2.99*sigma -> z = -2.99 -> no trigger
        assert check_1_3s(-2.99) is False

    def test_reject_above_threshold(self) -> None:
        # mu - 3.01*sigma -> z = -3.01 -> trigger
        assert check_1_3s(-3.01) is True

    def test_boundary_exact_3_does_not_trigger(self) -> None:
        assert check_1_3s(3.0) is False

    def test_positive_reject(self) -> None:
        assert check_1_3s(3.01) is True


# ---------------------------------------------------------------------------
# 2-2s  (reject rule)
# ---------------------------------------------------------------------------
class Test2_2s:
    def test_pass_second_point_not_over_2(self) -> None:
        # [mu + 2.10*sigma, mu + 1.90*sigma] => z = [2.10, 1.90] -> no trigger
        assert check_2_2s([2.10, 1.90]) is False

    def test_reject_both_over_2(self) -> None:
        # [mu + 2.10*sigma, mu + 2.20*sigma] => z = [2.10, 2.20] -> trigger
        assert check_2_2s([2.10, 2.20]) is True

    def test_reject_both_below_neg2(self) -> None:
        assert check_2_2s([-2.10, -2.20]) is True

    def test_opposite_sides_no_trigger(self) -> None:
        assert check_2_2s([2.10, -2.20]) is False

    def test_single_point_no_trigger(self) -> None:
        assert check_2_2s([2.50]) is False


# ---------------------------------------------------------------------------
# R-4s  (reject rule)
# ---------------------------------------------------------------------------
class TestR4s:
    def test_pass_spread_leq_4(self) -> None:
        # same run [mu + 2.10*sigma, mu - 1.80*sigma] => z = [2.10, -1.80]
        # spread = 2.10 - (-1.80) = 3.90 <= 4.0 -> no trigger
        assert check_r_4s([2.10, -1.80]) is False

    def test_reject_spread_gt_4(self) -> None:
        # same run [mu + 2.10*sigma, mu - 2.10*sigma] => z = [2.10, -2.10]
        # spread = 2.10 - (-2.10) = 4.20 > 4.0 -> trigger
        assert check_r_4s([2.10, -2.10]) is True

    def test_single_point_no_trigger(self) -> None:
        assert check_r_4s([2.50]) is False

    def test_both_positive_no_trigger(self) -> None:
        # Both on same side -- R-4s requires one > +2 and one < -2
        assert check_r_4s([2.50, 2.80]) is False


# ---------------------------------------------------------------------------
# 4-1s  (reject rule)
# ---------------------------------------------------------------------------
class Test4_1s:
    def test_pass_one_point_leq_1(self) -> None:
        # [mu + 1.10, mu + 1.20, mu + 0.95, mu + 1.30] -> z = [1.10, 1.20, 0.95, 1.30]
        # 0.95 is NOT > 1.0, so no trigger
        assert check_4_1s([1.10, 1.20, 0.95, 1.30]) is False

    def test_reject_all_above_1(self) -> None:
        # [mu + 1.10, mu + 1.20, mu + 1.05, mu + 1.30] -> z = [1.10, 1.20, 1.05, 1.30]
        # all > 1.0 -> trigger
        assert check_4_1s([1.10, 1.20, 1.05, 1.30]) is True

    def test_reject_all_below_neg1(self) -> None:
        assert check_4_1s([-1.10, -1.20, -1.05, -1.30]) is True

    def test_three_points_no_trigger(self) -> None:
        assert check_4_1s([1.10, 1.20, 1.30]) is False


# ---------------------------------------------------------------------------
# 10x  (reject rule)
# ---------------------------------------------------------------------------
class Test10x:
    def test_pass_9_consecutive_above(self) -> None:
        # 9 above mean -> no trigger
        assert check_10x([0.1] * 9) is False

    def test_reject_10_consecutive_above(self) -> None:
        # 10 above mean -> trigger
        assert check_10x([0.1] * 10) is True

    def test_reject_10_consecutive_below(self) -> None:
        assert check_10x([-0.1] * 10) is True

    def test_mixed_no_trigger(self) -> None:
        assert check_10x([0.1, -0.1, 0.1, -0.1, 0.1, -0.1, 0.1, -0.1, 0.1, -0.1]) is False


# ---------------------------------------------------------------------------
# evaluate_rules -- integration
# ---------------------------------------------------------------------------
class TestEvaluateRules:
    """Test the top-level evaluate_rules orchestrator."""

    def _config(self, r4s_enabled: bool = False, controls: int = 1) -> dict:
        return {"r4s_enabled": r4s_enabled, "controls_per_run": controls}

    # -- Status: pass --
    def test_all_pass(self) -> None:
        points = [_pt(25.5, idx=i) for i in range(5)]
        result = evaluate_rules(points, self._config())
        assert result["run_status"] == "pass"
        assert result["first_reject_rule"] is None
        assert result["warning_rules"] == []
        assert result["reject_rules"] == []

    # -- Status: warning (1-2s only) --
    def test_warning_only(self) -> None:
        # z = 2.01 -> 1-2s warning, but NOT 1-3s
        points = [_pt(MU + 2.01 * SD, idx=0)]
        result = evaluate_rules(points, self._config())
        assert result["run_status"] == "warning"
        assert "1-2s" in result["warning_rules"]
        assert result["reject_rules"] == []
        assert result["first_reject_rule"] is None

    # -- Status: reject (1-3s) --
    def test_reject_1_3s(self) -> None:
        points = [_pt(MU + 3.01 * SD, idx=0)]
        result = evaluate_rules(points, self._config())
        assert result["run_status"] == "reject"
        assert result["first_reject_rule"] == "1-3s"
        assert "1-3s" in result["reject_rules"]

    # -- Single-control assay does NOT trigger R-4s --
    def test_single_control_no_r4s(self) -> None:
        points = [
            _pt(MU + 2.10 * SD, level="L1", idx=0),
            _pt(MU - 2.10 * SD, level="L1", idx=1),
        ]
        result = evaluate_rules(points, self._config(r4s_enabled=False))
        # Should NOT have R-4s in reject_rules
        assert "R-4s" not in result["reject_rules"]

    # -- Multi-control assay triggers R-4s --
    def test_multi_control_r4s(self) -> None:
        points = [
            _pt(MU + 2.10 * SD, level="L1", idx=0),
            _pt(MU - 2.10 * SD, level="L2", idx=1),
        ]
        result = evaluate_rules(points, self._config(r4s_enabled=True, controls=2))
        assert "R-4s" in result["reject_rules"]
        assert result["run_status"] == "reject"

    # -- Evaluation continues after first reject (full violation capture) --
    def test_continues_after_reject(self) -> None:
        # First point triggers 1-3s, second point also triggers 1-3s
        points = [
            _pt(MU + 3.50 * SD, idx=0),
            _pt(MU + 3.20 * SD, idx=1),
        ]
        result = evaluate_rules(points, self._config())
        assert result["run_status"] == "reject"
        assert result["first_reject_rule"] == "1-3s"
        # Both points should have violations recorded
        violated_points = [v for v in result["violations"]]
        assert len(violated_points) >= 2

    # -- Run status precedence: reject > warning > pass --
    def test_status_precedence(self) -> None:
        # Point 1: z = 2.01 -> 1-2s warning
        # Point 2: z = 3.01 -> 1-3s reject (also 1-2s warning)
        points = [
            _pt(MU + 2.01 * SD, idx=0),
            _pt(MU + 3.01 * SD, idx=1),
        ]
        result = evaluate_rules(points, self._config())
        assert result["run_status"] == "reject"
        assert "1-2s" in result["warning_rules"]
        assert "1-3s" in result["reject_rules"]

    # -- 2-2s via evaluate_rules --
    def test_2_2s_via_evaluate(self) -> None:
        points = [
            _pt(MU + 2.10 * SD, idx=0),
            _pt(MU + 2.20 * SD, idx=1),
        ]
        result = evaluate_rules(points, self._config())
        assert "2-2s" in result["reject_rules"]

    # -- 4-1s via evaluate_rules --
    def test_4_1s_via_evaluate(self) -> None:
        points = [_pt(MU + 1.10 * SD, idx=i) for i in range(4)]
        result = evaluate_rules(points, self._config())
        assert "4-1s" in result["reject_rules"]
        assert result["run_status"] == "reject"

    # -- 10x via evaluate_rules --
    def test_10x_via_evaluate(self) -> None:
        points = [_pt(MU + 0.10 * SD, idx=i) for i in range(10)]
        result = evaluate_rules(points, self._config())
        assert "10x" in result["reject_rules"]
        assert result["run_status"] == "reject"

    # -- Evaluated points contain z-scores --
    def test_evaluated_points_have_z_scores(self) -> None:
        points = [_pt(26.0, idx=0)]  # z = 1.0
        result = evaluate_rules(points, self._config())
        assert len(result["evaluated_points"]) == 1
        assert result["evaluated_points"][0]["z_score"] == pytest.approx(1.0)

    # -- Summary stats populated --
    def test_summary_stats(self) -> None:
        points = [_pt(25.5, idx=0), _pt(26.0, idx=1)]
        result = evaluate_rules(points, self._config())
        stats = result["summary_stats"]
        assert "mean_z" in stats
        assert "max_z" in stats
        assert "min_z" in stats
        assert stats["point_count"] == 2
