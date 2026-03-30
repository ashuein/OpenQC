"""Pure Westgard multi-rule engine.

This module contains ONLY stateless logic -- no I/O, no database calls,
no imports from routers or repositories.  It depends solely on
``backend.utils.stats.z_score`` for the z-score calculation.
"""

from __future__ import annotations

from backend.utils.stats import z_score as _compute_z


# ---------------------------------------------------------------------------
# Individual rule checks (all pure)
# ---------------------------------------------------------------------------

def check_1_2s(z: float) -> bool:
    """Warning if |z| > 2.0.  Exact equality does NOT trigger."""
    return abs(z) > 2.0


def check_1_3s(z: float) -> bool:
    """Reject if |z| > 3.0.  Exact equality does NOT trigger."""
    return abs(z) > 3.0


def check_2_2s(z_scores: list[float]) -> bool:
    """Reject if 2 consecutive points both > 2.0 or both < -2.0."""
    if len(z_scores) < 2:
        return False
    a, b = z_scores[-2], z_scores[-1]
    return (a > 2.0 and b > 2.0) or (a < -2.0 and b < -2.0)


def check_r_4s(z_scores_in_run: list[float]) -> bool:
    """Reject if within same run, one point > +2.0 and another < -2.0,
    spread > 4.0 SD.  Only applies to multi-control assays."""
    if len(z_scores_in_run) < 2:
        return False
    for i in range(len(z_scores_in_run)):
        for j in range(i + 1, len(z_scores_in_run)):
            a, b = z_scores_in_run[i], z_scores_in_run[j]
            if (a > 2.0 and b < -2.0) or (a < -2.0 and b > 2.0):
                if abs(a - b) > 4.0:
                    return True
    return False


def check_4_1s(z_scores: list[float]) -> bool:
    """Reject if 4 consecutive points all > 1.0 or all < -1.0."""
    if len(z_scores) < 4:
        return False
    last4 = z_scores[-4:]
    return all(z > 1.0 for z in last4) or all(z < -1.0 for z in last4)


def check_10x(z_scores: list[float]) -> bool:
    """Reject if 10 consecutive points all strictly above or all strictly
    below mean (z=0)."""
    if len(z_scores) < 10:
        return False
    last10 = z_scores[-10:]
    return all(z > 0 for z in last10) or all(z < 0 for z in last10)


# ---------------------------------------------------------------------------
# Main evaluation entry-point
# ---------------------------------------------------------------------------

def evaluate_rules(points: list[dict], assay_config: dict) -> dict:
    """Evaluate all 6 Westgard rules on a sequence of QC points.

    Parameters
    ----------
    points : list[dict]
        Each dict must have keys: ``ct_value``, ``mean``, ``sd``,
        ``control_level``, ``sequence_index``.
        Points must be pre-sorted in canonical order.
    assay_config : dict
        Keys: ``r4s_enabled`` (bool), ``controls_per_run`` (int).

    Returns
    -------
    dict
        ``run_status``, ``first_reject_rule``, ``violations``,
        ``warning_rules``, ``reject_rules``, ``evaluated_points``,
        ``summary_stats``.
    """
    r4s_enabled = assay_config.get("r4s_enabled", False)

    evaluated_points: list[dict] = []
    violations: list[dict] = []
    warning_rules: list[str] = []
    reject_rules: list[str] = []
    first_reject_rule: str | None = None

    # Per-control-level z-score histories (for 2-2s, 4-1s, 10x)
    z_histories: dict[str, list[float]] = {}
    # z-scores within the current run across all levels (for R-4s)
    z_in_run: list[float] = []

    for pt in points:
        ct = pt["ct_value"]
        mu = pt["mean"]
        sigma = pt["sd"]
        level = pt["control_level"]
        idx = pt["sequence_index"]
        is_history = pt.get("_is_history", False)

        z = _compute_z(ct, mu, sigma)

        if level not in z_histories:
            z_histories[level] = []
        z_histories[level].append(z)
        z_in_run.append(z)

        level_history = z_histories[level]

        point_violations: list[str] = []

        # 1-2s (warning)
        if check_1_2s(z):
            point_violations.append("1-2s")
            if "1-2s" not in warning_rules:
                warning_rules.append("1-2s")

        # 1-3s (reject)
        if check_1_3s(z):
            point_violations.append("1-3s")
            if "1-3s" not in reject_rules:
                reject_rules.append("1-3s")
            if first_reject_rule is None:
                first_reject_rule = "1-3s"

        # 2-2s (reject) -- needs >= 2 points in the same control level
        if check_2_2s(level_history):
            point_violations.append("2-2s")
            if "2-2s" not in reject_rules:
                reject_rules.append("2-2s")
            if first_reject_rule is None:
                first_reject_rule = "2-2s"

        # R-4s (reject) -- only if enabled (multi-control assays), across levels
        if r4s_enabled and check_r_4s(z_in_run):
            point_violations.append("R-4s")
            if "R-4s" not in reject_rules:
                reject_rules.append("R-4s")
            if first_reject_rule is None:
                first_reject_rule = "R-4s"

        # 4-1s (reject) -- same control level
        if check_4_1s(level_history):
            point_violations.append("4-1s")
            if "4-1s" not in reject_rules:
                reject_rules.append("4-1s")
            if first_reject_rule is None:
                first_reject_rule = "4-1s"

        # 10x (reject) -- same control level
        if check_10x(level_history):
            point_violations.append("10x")
            if "10x" not in reject_rules:
                reject_rules.append("10x")
            if first_reject_rule is None:
                first_reject_rule = "10x"

        # Record violations for this point
        if point_violations:
            violation_entry: dict = {
                "sequence_index": idx,
                "control_level": level,
                "z_score": z,
                "rules": point_violations,
            }
            if is_history:
                violation_entry["_is_history"] = True
            violations.append(violation_entry)

        ep_entry: dict = {
            "cycle": idx,
            "control_level": level,
            "ct_value": ct,
            "mean": mu,
            "sd": sigma,
            "z_score": round(z, 6),
            "violations": point_violations,
        }
        if is_history:
            ep_entry["_is_history"] = True
        evaluated_points.append(ep_entry)

    # Determine overall run status
    if reject_rules:
        run_status = "reject"
    elif warning_rules:
        run_status = "warning"
    else:
        run_status = "pass"

    # Summary statistics
    all_z = [ep["z_score"] for ep in evaluated_points]
    summary_stats: dict = {}
    if all_z:
        summary_stats["mean_z"] = round(sum(all_z) / len(all_z), 6)
        summary_stats["max_z"] = round(max(all_z), 6)
        summary_stats["min_z"] = round(min(all_z), 6)
        summary_stats["point_count"] = len(all_z)
    # Include the control mean and SD used for this evaluation stream.
    # All points in a stream share the same assigned mean/SD from the
    # control lot, so take them from the first point.
    if evaluated_points:
        summary_stats["mean"] = evaluated_points[0]["mean"]
        summary_stats["sd"] = evaluated_points[0]["sd"]

    return {
        "run_status": run_status,
        "first_reject_rule": first_reject_rule,
        "violations": violations,
        "warning_rules": warning_rules,
        "reject_rules": reject_rules,
        "evaluated_points": evaluated_points,
        "summary_stats": summary_stats,
    }
