"""Assay validation engine -- pure calculation functions.

NO I/O, NO DB.  Only imports from backend.utils.stats.
"""

from __future__ import annotations

from backend.utils.stats import cv, linear_regression, mean, sd


def calculate_lod(blank_values: list[float]) -> dict:
    """LOD = mean + 3 * SD of blank/lowest-concentration replicates.

    Raises ValueError if fewer than 2 values provided.
    Returns: {"lod": float, "mean": float, "sd": float, "n": int}
    """
    if len(blank_values) < 2:
        raise ValueError(
            "LOD calculation requires at least 2 blank replicate values"
        )
    m = mean(blank_values)
    s = sd(blank_values)
    return {"lod": m + 3 * s, "mean": m, "sd": s, "n": len(blank_values)}


def calculate_loq(
    concentration_data: list[dict], cv_threshold: float
) -> dict:
    """Find lowest concentration where CV <= threshold.

    Args:
        concentration_data: list of {"concentration": float, "replicates": list[float]}
                           sorted by concentration ascending.
        cv_threshold: maximum acceptable CV (percentage).

    Returns:
        {"loq": float|None, "cv_at_loq": float|None, "all_concentrations": list[dict]}
        Each entry: {"concentration": float, "cv": float, "n": int, "meets_threshold": bool}
    """
    all_concentrations: list[dict] = []
    loq_value: float | None = None
    cv_at_loq: float | None = None

    for entry in concentration_data:
        conc = entry["concentration"]
        reps = entry["replicates"]
        if len(reps) < 2:
            raise ValueError(
                f"Concentration {conc} has fewer than 2 replicates; "
                "cannot compute CV"
            )
        c = cv(reps)
        meets = c <= cv_threshold
        all_concentrations.append(
            {
                "concentration": conc,
                "cv": c,
                "n": len(reps),
                "meets_threshold": meets,
            }
        )
        if meets and loq_value is None:
            loq_value = conc
            cv_at_loq = c

    return {
        "loq": loq_value,
        "cv_at_loq": cv_at_loq,
        "all_concentrations": all_concentrations,
    }


def calculate_intra_run_precision(replicates: list[float]) -> dict:
    """CV across replicates within a single run.

    Raises ValueError if fewer than 2 replicates.
    Returns: {"cv": float, "mean": float, "sd": float, "n": int}
    """
    if len(replicates) < 2:
        raise ValueError(
            "Intra-run precision requires at least 2 replicates"
        )
    m = mean(replicates)
    s = sd(replicates)
    c = cv(replicates)
    return {"cv": c, "mean": m, "sd": s, "n": len(replicates)}


def calculate_inter_run_precision(run_means: list[dict]) -> dict:
    """CV across run means from multiple runs.

    Args:
        run_means: list of {"run_id": str, "mean": float, "date": str}

    Returns:
        {"cv": float, "mean": float, "sd": float, "n_runs": int,
         "status": "evaluated"|"not_evaluated"}
        Returns status "not_evaluated" if fewer than 3 runs.
    """
    n = len(run_means)
    if n < 3:
        return {
            "cv": 0.0,
            "mean": 0.0,
            "sd": 0.0,
            "n_runs": n,
            "status": "not_evaluated",
        }

    values = [r["mean"] for r in run_means]
    m = mean(values)
    s = sd(values)
    c = cv(values)
    return {"cv": c, "mean": m, "sd": s, "n_runs": n, "status": "evaluated"}


def calculate_linearity(levels: list[dict]) -> dict:
    """Linear regression across dilution series.

    Args:
        levels: list of {"expected": float, "measured": float}

    Raises ValueError if fewer than 3 levels.
    Returns: {"slope": float, "intercept": float, "r_squared": float, "n_levels": int}
    """
    if len(levels) < 3:
        raise ValueError("Linearity calculation requires at least 3 levels")

    x = [lvl["expected"] for lvl in levels]
    y = [lvl["measured"] for lvl in levels]
    reg = linear_regression(x, y)
    return {
        "slope": reg["slope"],
        "intercept": reg["intercept"],
        "r_squared": reg["r_squared"],
        "n_levels": len(levels),
    }


def evaluate_acceptance(results: dict, criteria: dict) -> dict:
    """Apply user-defined acceptance criteria to validation results.

    Args:
        results: dict of metric_name -> value
            (e.g. {"lod": 100.5, "intra_cv": 3.2, "r_squared": 0.998})
        criteria: dict of metric_name -> {"threshold": float, "operator": "lte"|"gte"}

    Returns:
        {
            "overall_status": "pass"|"fail",
            "details": {metric: {"value": float, "threshold": float,
                                  "operator": str, "status": "pass"|"fail"}}
        }
    """
    details: dict = {}
    overall = "pass"

    for metric_name, criterion in criteria.items():
        value = results.get(metric_name)
        threshold = criterion["threshold"]
        operator = criterion["operator"]

        if value is None:
            details[metric_name] = {
                "value": None,
                "threshold": threshold,
                "operator": operator,
                "status": "fail",
            }
            overall = "fail"
            continue

        if operator == "lte":
            status = "pass" if value <= threshold else "fail"
        elif operator == "gte":
            status = "pass" if value >= threshold else "fail"
        else:
            raise ValueError(f"Unknown operator: {operator!r}")

        if status == "fail":
            overall = "fail"

        details[metric_name] = {
            "value": value,
            "threshold": threshold,
            "operator": operator,
            "status": status,
        }

    return {"overall_status": overall, "details": details}
