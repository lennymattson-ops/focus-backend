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
    Classify outcome scores generated from
    normalized behavioral state changes.
    """

    if score >= 0.40:
        return "Strong improvement"

    if score >= 0.20:
        return "Improvement"

    if score >= 0.05:
        return "Minor improvement"

    if score > -0.05:
        return "No significant change"

    if score > -0.20:
        return "Minor regression"

    if score > -0.40:
        return "Regression"

    return "Strong regression"

# ---------------------------------------------------------
# Phase 14.0
# Compliance Tracking (Doc 3 - FIG. 9)
# ---------------------------------------------------------

def compute_compliance(answer):
    """
    Convert the user's answer to "Did you try the
    suggested intervention?" into a score.

    "yes"     -> 1.0  (did the intervention)
    "partial" -> 0.5  (did some of it)
    "no"      -> 0.0  (did not do it)

    Any unexpected value falls back to 0.0 so a
    bad payload can never crash the loop.
    """

    mapping = {
        "yes": 1.0,
        "partial": 0.5,
        "no": 0.0,
    }

    return mapping.get(
        str(answer).lower().strip(),
        0.0,
    )


def measure_compliance(data):
    """
    Real compliance measurement based on the user's
    answer (Doc 3 - Behavioral Compliance Measurement).

    Previously this faked compliance by returning the
    current consistency score, which had nothing to do
    with whether the user actually did the intervention.
    """

    return compute_compliance(
        data.get("compliance", "no")
    )

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
