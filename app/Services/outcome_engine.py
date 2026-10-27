def calculate_outcome(previous_state, new_state):
    """
    Measures improvement or regression between two behavioral states.
    Returns a score from -100 to +100.
    """

    motivation_change = new_state["motivation"] - previous_state["motivation"]
    energy_change = new_state["energy"] - previous_state["energy"]
    consistency_change = new_state["consistency"] - previous_state["consistency"]
    risk_change = previous_state["risk"] - new_state["risk"]  # lower risk = improvement

    score = (
        (motivation_change * 0.3) +
        (energy_change * 0.3) +
        (consistency_change * 0.3) +
        (risk_change * 0.1)
    )

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


def measure_compliance(data):
    """
    Basic compliance scoring.
    """

    completed = data.get("completed", True)
    return 1.0 if completed else 0.0


def process_outcome(data):
    """
    Unified outcome engine:
    - numeric outcome scoring
    - outcome classification
    - compliance scoring
    """

    previous_state = data.get("previous_state", {})
    current_state = data.get("current_state", {})

    # Numeric outcome score
    numeric_score = calculate_outcome(previous_state, current_state)
    category = classify_outcome(numeric_score)

    # Compliance score
    compliance_score = measure_compliance(data)

    return {
        "numeric_score": numeric_score,
        "category": category,
        "compliance_score": compliance_score
    }
