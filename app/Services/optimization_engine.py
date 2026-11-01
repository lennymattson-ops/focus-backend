from typing import List, Dict
import random

from app.Services.drift_detector import detect_behavioral_drift


# ---------------------------------------------------------
# Phase 10.8
# Starvation Protection
# ---------------------------------------------------------

MIN_WEIGHT_FLOOR = 0.08


def update_intervention_weights(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    learning_rate: float = 0.05,
):
    """
    Learning Engine

    Long-term memory:
        weight

    Short-term memory:
        confidence

    Repetition memory:
        fatigue
    """

    updated = []

    overall = effectiveness_history.get(
        "overall",
        0
    )

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

        # Confidence decay
        new_confidence = (
            current_confidence * 0.90
        )

        new_fatigue = current_fatigue

        if intervention["name"] == selected_name:

            adjustment = (
                overall * learning_rate
            )

            new_weight = (
                current_weight
                + adjustment
            )

            # -------------------------------------------------
            # Phase 10.9
            # Confidence Momentum
            # -------------------------------------------------

            confidence_delta = (
                overall * 0.05
            )

            # Strong outcomes should
            # produce stronger confidence shifts.
            if abs(overall) >= 1.5:
                confidence_delta *= 1.25

            new_confidence += confidence_delta

            # Fatigue build-up
            new_fatigue += 1

        else:

            # Fatigue recovery
            new_fatigue = max(
                0,
                current_fatigue - 1
            )

        # -------------------------------------------------
        # Phase 10.8
        # Starvation Protection
        # -------------------------------------------------

        new_weight = max(
            MIN_WEIGHT_FLOOR,
            min(new_weight, 1.0)
        )

        new_confidence = max(
            -0.25,
            min(new_confidence, 0.25)
        )

        new_fatigue = min(
            new_fatigue,
            10
        )

        updated.append({
            **intervention,
            "weight": round(
                new_weight,
                3
            ),
            "confidence": round(
                new_confidence,
                3
            ),
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
                    intervention["weight"]
                    / total,
                    3
                )
            })

        return normalized

    return updated


def drift_aware_score(
    intervention: Dict,
    drift: Dict,
    analysis: Dict = None,
):
    """
    Final ranking score.

    Components:
    - Weight
    - Confidence
    - Fatigue
    - Drift bonuses
    - Decision alignment bonuses
    """

    fatigue = intervention.get(
        "fatigue",
        0
    )

    # -------------------------------------------------
    # Phase 10.8
    # Stronger Fatigue Balancing
    # -------------------------------------------------

    fatigue_penalty = (
        fatigue * 0.12
    )

    if fatigue >= 4:
        fatigue_penalty += 0.20

    if fatigue >= 6:
        fatigue_penalty += 0.15

    score = (
        intervention.get(
            "weight",
            0
        )
        + intervention.get(
            "confidence",
            0
        )
        - fatigue_penalty
    )

    tags = intervention.get(
        "tags",
        []
    )

    # -------------------------
    # Drift Bonuses
    # -------------------------

    if (
        drift.get("motivation")
        == "decreasing"
        and
        "motivation_support"
        in tags
    ):
        score += 0.10

    if (
        drift.get("consistency")
        == "decreasing"
        and
        "routine"
        in tags
    ):
        score += 0.10

    if (
        drift.get("risk")
        == "increasing"
        and
        "risk_reduction"
        in tags
    ):
        score += 0.10

    if drift.get(
        "intervention_fatigue"
    ):
        score -= 0.15

    # -------------------------
    # Decision Alignment
    # -------------------------

    if analysis:

        risks = analysis.get(
            "risks",
            []
        )

        if (
            "Low motivation"
            in risks
            and
            "motivation_support"
            in tags
        ):
            score += 0.15

        if (
            "Low energy"
            in risks
            and
            "energy_support"
            in tags
        ):
            score += 0.15

        if (
            "Inconsistent behavior"
            in risks
            and (
                "routine"
                in tags
                or
                "consistency_support"
                in tags
            )
        ):
            score += 0.15

        if (
            "High risk"
            in risks
            and
            "risk_reduction"
            in tags
        ):
            score += 0.15

    return score


def select_intervention(
    interventions: List[Dict],
    drift: Dict,
    analysis: Dict = None,
    exploration_rate: float = 0.15,
):
    """
    Selection Engine

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
                drift,
                analysis
            )
        )
        for intervention in interventions
    ]

    scored.sort(
        key=lambda x: x[1],
        reverse=True
    )

    if (
        random.random()
        < exploration_rate
    ):

        alternatives = [
            item[0]
            for item in scored[1:]
        ]

        if alternatives:
            return random.choice(
                alternatives
            )

    return scored[0][0]


def optimize(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    full_history: List[Dict] = None,
    decision_analysis: Dict = None,
):
    """
    Phase 10.9 Optimization Pipeline
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
        drift,
        decision_analysis,
    )

    return {
        "updated_interventions": updated,
        "selected_intervention": best,
        "effectiveness_history": effectiveness_history,
        "drift": drift,
    }