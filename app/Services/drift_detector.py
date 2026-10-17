from typing import List, Dict


def compute_trend(values: List[float]) -> str:
    if len(values) < 2:
        return "stable"

    delta = values[-1] - values[0]

    if delta > 0.1:
        return "increasing"
    elif delta < -0.1:
        return "decreasing"
    else:
        return "stable"


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

    motivation_values = [h["current_state"]["motivation"] for h in history]
    energy_values = [h["current_state"]["energy"] for h in history]
    consistency_values = [h["current_state"]["consistency"] for h in history]
    risk_values = [h["current_state"]["risk"] for h in history]

    effectiveness_values = [
        h.get("effectiveness_history", {}).get("overall", 0.5)
        for h in history
    ]

    drift = {
        "motivation": compute_trend(motivation_values),
        "energy": compute_trend(energy_values),
        "consistency": compute_trend(consistency_values),
        "risk": compute_trend(risk_values),
        "effectiveness": compute_trend(effectiveness_values),
    }

    drift["intervention_fatigue"] = (
        drift["effectiveness"] == "decreasing"
        and drift["consistency"] == "decreasing"
    )

    return drift
