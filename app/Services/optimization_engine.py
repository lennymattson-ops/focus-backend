from typing import List, Dict
import random

from app.Services.drift_detector import detect_behavioral_drift


def update_intervention_weights(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    learning_rate: float = 0.05,
):
    """
    Phase 9.3.1 Learning Engine

    Long-term memory:
        weight

    Short-term memory:
        confidence

    Only the selected intervention is rewarded
    or penalized based on effectiveness.

    All weights are normalized after updates.
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

        current_confidence = intervention.get(
            "confidence",
            0.0
        )

        new_weight = current_weight
        new_confidence = current_confidence

        if intervention["name"] == selected_name:

            # Long-term learning
            adjustment = overall * learning_rate
            new_weight = current_weight + adjustment

            # Phase 9.3.1 Confidence Scaling
            confidence_delta = overall * 0.02
            new_confidence += confidence_delta

        # Weight protection
        new_weight = max(
            0.05,
            min(new_weight, 1.0)
        )

        # Confidence protection
        new_confidence = max(
            -0.25,
            min(new_confidence, 0.25)
        )

        updated.append({
            **intervention,
            "weight": round(new_weight, 3),
            "confidence": round(new_confidence, 3)
        })

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
    Final ranking score.

    Uses:
    - Weight (long-term learning)
    - Confidence (recent success)
    - Drift bonuses
    """

    score = (
        intervention.get("weight", 0)
        + intervention.get("confidence", 0)
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


def select_intervention(
    interventions: List[Dict],
    drift: Dict,
    exploration_rate: float = 0.15,
):
    """
    Phase 9.2 + 9.3 + 9.3.1

    85%:
        exploit best option

    15%:
        explore alternatives
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

    # Exploration Mode
    if random.random() < exploration_rate:

        alternatives = [
            item[0]
            for item in scored[1:]
        ]

        if alternatives:
            return random.choice(alternatives)

    # Exploitation Mode
    return scored[0][0]


def optimize(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    full_history: List[Dict] = None,
):
    """
    Phase 9.3.1 Optimization Pipeline
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