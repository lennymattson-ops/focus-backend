from typing import List, Dict
from app.Services.drift_detector import detect_behavioral_drift
from app.Services.interventions import INTERVENTIONS


def update_intervention_weights(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    learning_rate: float = 0.1,
):
    """
    Adaptive weight learning for Phase 9.

    - Supports effectiveness as float OR list[float]
    - Moves weight toward effectiveness
    - Normalizes weights for stability
    """

    updated = []

    for intervention in interventions:
        name = intervention["name"]
        weight = intervention.get("weight", 1.0)

        raw = effectiveness_history.get(
            name,
            effectiveness_history.get("overall", 0.5)
        )

        if isinstance(raw, list):
            effectiveness = sum(raw) / len(raw) if len(raw) > 0 else 0.5
        else:
            effectiveness = raw

        delta = (effectiveness - 0.5) * learning_rate
        new_weight = weight + delta

        new_weight = max(0.0, min(new_weight, 2.0))

        updated.append({
            **intervention,
            "weight": round(new_weight, 3)
        })

    total = sum(i["weight"] for i in updated)
    if total > 0:
        normalized = [
            {**i, "weight": round(i["weight"] / total, 3)}
            for i in updated
        ]
    else:
        normalized = updated

    return normalized


def drift_aware_score(intervention: Dict, drift: Dict):
    """
    Adjusts intervention preference based on drift signals.

    Example idea:
    - If motivation is decreasing, favor interventions tagged as "motivation_support"
    - If consistency is decreasing, favor "routine" or "structure" interventions
    - If intervention_fatigue is True, slightly penalize all interventions
    """

    base = intervention.get("weight", 0.0)
    tags = intervention.get("tags", [])

    score = base

    if drift.get("motivation") == "decreasing" and "motivation_support" in tags:
        score += 0.1

    if drift.get("consistency") == "decreasing" and "routine" in tags:
        score += 0.1

    if drift.get("risk") == "increasing" and "risk_reduction" in tags:
        score += 0.1

    if drift.get("intervention_fatigue"):
        score -= 0.05

    return score


def select_intervention(interventions: List[Dict], drift: Dict):
    """
    Drift-aware intervention selection:
    - Uses weight as base
    - Adjusts preference based on drift signals
    """

    if not interventions:
        return None

    scored = [
        (intervention, drift_aware_score(intervention, drift))
        for intervention in interventions
    ]

    best, _ = max(scored, key=lambda x: x[1])
    return best


def optimize(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    full_history: List[Dict] = None
):
    """
    Phase 9 Step 6 Optimization Pipeline:
    - Adaptive weight learning
    - Behavioral drift detection
    - Drift-aware intervention selection
    """

    updated = update_intervention_weights(interventions, effectiveness_history)
    drift = detect_behavioral_drift(full_history or [])
    best = select_intervention(updated, drift)

    return {
        "updated_interventions": updated,
        "selected_intervention": best,
        "effectiveness_history": effectiveness_history,
        "drift": drift
    }
