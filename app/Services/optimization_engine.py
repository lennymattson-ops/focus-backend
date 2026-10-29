from typing import List, Dict
from app.Services.drift_detector import detect_behavioral_drift


def update_intervention_weights(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    learning_rate: float = 0.05,
):
    """
    Phase 9.1 Learning Engine

    Only the selected intervention is rewarded or penalized.

    Positive effectiveness:
        selected intervention weight increases

    Negative effectiveness:
        selected intervention weight decreases

    Remaining interventions stay unchanged.

    Finally normalize weights so total = 1.
    """

    updated = []

    overall = effectiveness_history.get("overall", 0)

    selected_name = effectiveness_history.get(
        "selected_intervention"
    )

    for intervention in interventions:

        current_weight = intervention.get(
            "weight",
            0.167
        )

        new_weight = current_weight

        # ONLY update the intervention that was used
        if intervention["name"] == selected_name:

            adjustment = overall * learning_rate

            new_weight = current_weight + adjustment

        # Prevent collapse
        new_weight = max(
            0.05,
            min(new_weight, 1.0)
        )

        updated.append({
            **intervention,
            "weight": round(new_weight, 3)
        })

    # Normalize weights
    total = sum(
        i["weight"]
        for i in updated
    )

    if total > 0:

        normalized = []

        for intervention in updated:

            normalized.append({
                **intervention,
                "weight": round(
                    intervention["weight"] / total,
                    3
                )
            })

        return normalized

    return updated


def drift_aware_score(
    intervention: Dict,
    drift: Dict
):
    """
    Boost interventions that match drift signals.
    """

    score = intervention.get(
        "weight",
        0
    )

    tags = intervention.get(
        "tags",
        []
    )

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


import random


def select_intervention(
    interventions: List[Dict],
    drift: Dict,
    exploration_rate: float = 0.15
):
    """
    Phase 9.2 Exploration Strategy

    85%:
        Choose the best intervention

    15%:
        Explore a different intervention
    """

    if not interventions:
        return None

    scored = [
        (
            intervention,
            drift_aware_score(
                intervention,
                drift
            )
        )
        for intervention in interventions
    ]

    scored.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Exploration
    if random.random() < exploration_rate:

        # Choose from everything except current best
        alternatives = [
            item[0]
            for item in scored[1:]
        ]

        if alternatives:
            return random.choice(alternatives)

    # Exploitation (normal behavior)
    return scored[0][0]


def optimize(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    full_history: List[Dict] = None,
):
    """
    Phase 9.1 Optimization Pipeline
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