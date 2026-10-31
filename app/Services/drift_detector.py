from typing import List, Dict


TREND_THRESHOLD = 0.10
WINDOW_SIZE = 3
EPSILON = 0.001


def classify_delta(delta: float) -> str:
    """
    Handle floating-point precision issues.

    Example:
    -0.09999999999999998 should still be treated
    as a meaningful decrease when threshold is 0.10.
    """

    if delta >= (TREND_THRESHOLD - EPSILON):
        return "increasing"

    if delta <= (-TREND_THRESHOLD + EPSILON):
        return "decreasing"

    return "stable"


def compute_trend(values: List[float]) -> str:
    """
    Detect trend using rolling window averages.

    For small histories:
    compare the two most recent values.

    For larger histories:
    compare previous rolling average
    against recent rolling average.
    """

    if len(values) < WINDOW_SIZE * 2:
        if len(values) < 2:
            return "stable"

        delta = values[-1] - values[-2]

        return classify_delta(delta)

    previous_window = values[-(WINDOW_SIZE * 2):-WINDOW_SIZE]
    recent_window = values[-WINDOW_SIZE:]

    previous_avg = sum(previous_window) / len(previous_window)
    recent_avg = sum(recent_window) / len(recent_window)

    delta = recent_avg - previous_avg

    return classify_delta(delta)


def detect_behavioral_drift(history: List[Dict]) -> Dict:
    if len(history) < 2:
        return {
            "motivation": "stable",
            "energy": "stable",
            "consistency": "stable",
            "risk": "stable",
            "effectiveness": "stable",
            "intervention_fatigue": False,
        }

    motivation_values = [
        h["current_state"]["motivation"]
        for h in history
    ]

    energy_values = [
        h["current_state"]["energy"]
        for h in history
    ]

    consistency_values = [
        h["current_state"]["consistency"]
        for h in history
    ]

    risk_values = [
        h["current_state"]["risk"]
        for h in history
    ]

    effectiveness_values = [
        h.get("effectiveness_history", {}).get("overall", 0)
        for h in history
    ]

    drift = {
        "motivation": compute_trend(motivation_values),
        "energy": compute_trend(energy_values),
        "consistency": compute_trend(consistency_values),
        "risk": compute_trend(risk_values),
        "effectiveness": compute_trend(effectiveness_values),
    }

    recent_effectiveness = (
        effectiveness_values[-3:]
        if len(effectiveness_values) >= 3
        else effectiveness_values
    )

    average_effectiveness = (
        sum(recent_effectiveness) / len(recent_effectiveness)
        if recent_effectiveness
        else 0
    )

    drift["intervention_fatigue"] = (
        average_effectiveness < 0
        and drift["consistency"] == "decreasing"
    )

    return drift