"""
Pure math / statistics helpers for QC calculations.

All functions are stateless -- no I/O, no database access.
"""

from __future__ import annotations

import math


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of *values*.

    Raises
    ------
    ValueError
        If *values* is empty.
    """
    if not values:
        raise ValueError("mean requires at least one value")
    return sum(values) / len(values)


def sd(values: list[float], ddof: int = 1) -> float:
    """Return the standard deviation of *values*.

    Parameters
    ----------
    values : list[float]
        Sample values.
    ddof : int, optional
        Delta degrees of freedom.  ``1`` (default) gives the *sample*
        standard deviation; ``0`` gives the *population* standard deviation.

    Raises
    ------
    ValueError
        If *values* is empty or has fewer elements than ``ddof + 1``.
    """
    if not values:
        raise ValueError("sd requires at least one value")
    n = len(values)
    if n <= ddof:
        raise ValueError(
            f"sd with ddof={ddof} requires at least {ddof + 1} values, got {n}"
        )
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / (n - ddof)
    return math.sqrt(variance)


def cv(values: list[float]) -> float:
    """Return the coefficient of variation as a percentage (SD / mean * 100).

    If the mean is zero, returns ``float('inf')``.

    Raises
    ------
    ValueError
        If *values* has fewer than 2 elements (sample SD is undefined).
    """
    m = mean(values)  # propagates ValueError on empty list
    s = sd(values)
    if m == 0.0:
        return float("inf")
    return (s / m) * 100.0


def z_score(value: float, mean: float, sd: float) -> float:
    """Return the z-score: ``(value - mean) / sd``.

    Raises
    ------
    ValueError
        If *sd* is zero.
    """
    if sd == 0.0:
        raise ValueError("z_score requires a non-zero standard deviation")
    return (value - mean) / sd


def linear_regression(x: list[float], y: list[float]) -> dict:
    """Ordinary least-squares linear regression.

    Parameters
    ----------
    x, y : list[float]
        Paired observations.  Must be the same length and contain at
        least 2 points.

    Returns
    -------
    dict
        ``{"slope": float, "intercept": float, "r_squared": float}``

    Raises
    ------
    ValueError
        If lists differ in length or contain fewer than 2 points.
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    n = len(x)
    if n < 2:
        raise ValueError("linear_regression requires at least 2 data points")

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    ss_xx = sum((xi - mean_x) ** 2 for xi in x)
    ss_yy = sum((yi - mean_y) ** 2 for yi in y)
    ss_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))

    if ss_xx == 0.0:
        raise ValueError("All x values are identical; slope is undefined")

    slope = ss_xy / ss_xx
    intercept = mean_y - slope * mean_x

    r_squared = (ss_xy**2) / (ss_xx * ss_yy) if ss_yy != 0.0 else 1.0

    return {"slope": slope, "intercept": intercept, "r_squared": r_squared}
