def calculate_outcome(previous_state, new_state):
    """
    Measures improvement or regression between two behavioral states.
    Returns a score from -100 to +100.
    """

    # Compare key metrics
    motivation_change = new_state["motivation"] - previous_state["motivation"]
    energy_change = new_state["energy"] - previous_state["energy"]
    consistency_change = new_state["consistency"] - previous_state["consistency"]
    risk_change = previous_state["risk"] - new_state["risk"]  # lower risk = improvement

    # Weighted scoring model
    score = (
        (motivation_change * 0.3) +
        (energy_change * 0.3) +
        (consistency_change * 0.3) +
        (risk_change * 0.1)
    )

    # Clamp score between -100 and +100
    score = max(min(score, 100), -100)

    return round(score, 2)


def classify_outcome(score):
    """
    Converts a numeric score into a human-readable category.
    """

    if score >= 50:
        return "Strong improvement"
    if score >= 20:
        return "Moderate improvement"
    if score >= 5:
        return "Slight improvement"
    if score > -5:
        return "No significant change"
    if score > -20:
        return "Slight regression"
    if score > -50:
        return "Moderate regression"
    return "Strong regression"
