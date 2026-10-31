from typing import List, Dict
import random

from app.Services.drift_detector import detect_behavioral_drift


def update_intervention_weights(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    learning_rate: float = 0.05,
):
    """
    Phase 9.5 Learning Engine

    Long-term memory:
        weight

    Short-term memory:
        confidence

    Repetition memory:
        fatigue
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

        current_fatigue = intervention.get(
            "fatigue",
            0
        )

        new_weight = current_weight

        # Phase 9.4 Confidence Decay
        new_confidence = current_confidence * 0.90

        new_fatigue = current_fatigue

        if intervention["name"] == selected_name:

            # Long-term learning
            adjustment = overall * learning_rate
            new_weight = current_weight + adjustment

            # Phase 9.3.1 Confidence Scaling
            confidence_delta = overall * 0.02
            new_confidence += confidence_delta

            # Phase 9.5 Fatigue Build-Up
            new_fatigue += 1

        else:

            # Recover fatigue for unused interventions
            new_fatigue = max(
                0,
                current_fatigue - 1
            )

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

        # Fatigue protection
        new_fatigue = min(
            new_fatigue,
            10
        )

        updated.append({
            **intervention,
            "weight": round(new_weight, 3),
            "confidence": round(new_confidence, 3),
            "fatigue": new_fatigue
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

    Components:
    - Weight
    - Confidence
    - Fatigue penalty
    - Drift bonuses
    """

    fatigue = intervention.get(
        "fatigue",
        0
    )

    # Phase 10.4 Fatigue-Aware Selection
    fatigue_penalty = fatigue * 0.08

    # Exhaustion penalties
    if fatigue >= 4:
        fatigue_penalty += 0.15

    if fatigue >= 6:
        fatigue_penalty += 0.10

    score = (
        intervention.get("weight", 0)
        + intervention.get("confidence", 0)
        - fatigue_penalty
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

    # Phase 10.4 Global Fatigue Response
    if drift.get("intervention_fatigue"):
        score -= 0.15

    return score


def select_intervention(
    interventions: List[Dict],
    drift: Dict,
    exploration_rate: float = 0.15,
):
    """
    Phase 9.2 + 9.3 + 9.4 + 9.5 + 10.4

    85% exploit
    15% explore
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

    # Exploration mode
    if random.random() < exploration_rate:

        alternatives = [
            item[0]
            for item in scored[1:]
        ]

        if alternatives:
            return random.choice(alternatives)

    # Exploitation mode
    return scored[0][0]


def optimize(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    full_history: List[Dict] = None,
):
    """
    Phase 10.4 Optimization Pipeline
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