"""Sigma analysis engine — pure calculation functions."""


def calculate_sigma(tea_percent: float, bias_percent: float, cv_percent: float) -> dict:
    """
    Calculate Sigma score, classification, NMEDx coordinates, and recommended rules.

    Args:
        tea_percent: Total Allowable Error (percentage, must be > 0)
        bias_percent: Bias (percentage, must be >= 0)
        cv_percent: Coefficient of Variation (percentage, must be > 0)

    Returns:
        dict with: sigma_score, classification, recommended_rules, nmedx_x, nmedx_y, notes

    Raises:
        ValueError: if inputs fail validation
    """
    # Validate inputs
    if cv_percent <= 0:
        raise ValueError("cv_percent must be > 0")
    if tea_percent <= 0:
        raise ValueError("tea_percent must be > 0")
    if bias_percent < 0:
        raise ValueError("bias_percent must be >= 0")

    sigma_score = (tea_percent - bias_percent) / cv_percent
    classification = classify_sigma(sigma_score)
    recommended_rules, notes = get_recommended_rules(sigma_score)
    nmedx_x = bias_percent / tea_percent
    nmedx_y = cv_percent / tea_percent

    return {
        "sigma_score": round(sigma_score, 2),
        "classification": classification,
        "recommended_rules": recommended_rules,
        "nmedx_x": round(nmedx_x, 4),
        "nmedx_y": round(nmedx_y, 4),
        "notes": notes,
    }


def classify_sigma(sigma_score: float) -> str:
    """Classify sigma score into bands."""
    if sigma_score >= 6.0:
        return "world_class"
    elif sigma_score >= 5.0:
        return "excellent"
    elif sigma_score >= 4.0:
        return "good"
    elif sigma_score >= 3.0:
        return "marginal"
    else:
        return "unacceptable"


def get_recommended_rules(sigma_score: float) -> tuple[list[str], str | None]:
    """Return (recommended_rules, notes) based on sigma band."""
    if sigma_score >= 6.0:
        return ["1-3s"], None
    elif sigma_score >= 5.0:
        return ["1-3s", "2-2s", "R-4s"], None
    elif sigma_score >= 4.0:
        return ["1-3s", "2-2s", "R-4s", "4-1s", "10x"], None
    elif sigma_score >= 3.0:
        return ["1-3s", "2-2s", "R-4s", "4-1s", "10x"], "Intensified QC and shorter review interval recommended"
    else:
        return [], "Method unacceptable until corrected"


def calculate_batch(inputs: list[dict]) -> list[dict]:
    """Calculate sigma for a batch of assay inputs.

    Args:
        inputs: list of dicts with keys: assay, tea_percent, bias_percent, cv_percent

    Returns:
        list of result dicts, each with: assay, sigma_score, classification,
        recommended_rules, nmedx_x, nmedx_y, notes
    """
    results = []
    for item in inputs:
        result = calculate_sigma(item["tea_percent"], item["bias_percent"], item["cv_percent"])
        result["assay"] = item["assay"]
        results.append(result)
    return results
