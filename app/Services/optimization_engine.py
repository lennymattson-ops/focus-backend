from typing import List, Dict
from app.Services.drift_detector import detect_behavioral_drift


def update_intervention_weights(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    learning_rate: float = 0.05,
):
    """
    Adaptive weight learning.

    Prevents weights from collapsing to zero and keeps
    intervention ranking stable over time.
    """

    updated = []

    overall = effectiveness_history.get("overall", 0)

    for intervention in interventions:
        current_weight = intervention.get("weight", 0.167)

        # Small reward / penalty
        adjustment = overall * learning_rate

        new_weight = current_weight + adjustment

        # Prevent weight collapse
        new_weight = max(0.05, min(new_weight, 1.0))

        updated.append({
            **intervention,
            "weight": round(new_weight, 3)
        })

    total = sum(i["weight"] for i in updated)

    normalized = [
        {
            **i,
            "weight": round(i["weight"] / total, 3)
        }
        for i in updated
    ]

    return normalized


def drift_aware_score(intervention: Dict, drift: Dict):
    """
    Adjust intervention ranking based on drift.
    """

    score = intervention.get("weight", 0)

    tags = intervention.get("tags", [])

    if (
        drift.get("motivation") == "decreasing"
        and "motivation_support" in tags
    ):
        score += 0.10

    if (
        drift.get("consistency") == "decreasing"
        and "routine" in tags
    ):
        score += 0.10

    if (
        drift.get("risk") == "increasing"
        and "risk_reduction" in tags
    ):
        score += 0.10

    if drift.get("intervention_fatigue"):
        score -= 0.05

    return score


def select_intervention(
    interventions: List[Dict],
    drift: Dict
):
    """
    Select highest scoring intervention.
    """

    if not interventions:
        return None

    scored = [
        (
            intervention,
            drift_aware_score(intervention, drift)
        )
        for intervention in interventions
    ]

    best, _ = max(
        scored,
        key=lambda x: x[1]
    )

    return best


def optimize(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    full_history: List[Dict] = None,
):
    """
    Optimization pipeline.
    """

    updated = update_intervention_weights(
        interventions,
        effectiveness_history,
    )

    drift = detect_behavioral_drift(
        full_history or []
    )

    best = select_intervention(
        updated,
        drift
    )

    return {
        "updated_interventions": updated,
        "selected_intervention": best,
        "effectiveness_history": effectiveness_history,
        "drift": drift,
    }