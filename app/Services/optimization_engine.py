from typing import List, Dict


def update_intervention_weights(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    learning_rate: float = 0.1,
):
    """
    Adjusts intervention weights based on historical effectiveness.

    interventions: list of { "name": str, "weight": float }
    effectiveness_history: { intervention_name: float OR list[float] }
    """

    updated = []

    for intervention in interventions:
        iid = intervention["name"]  # use name as the identifier
        weight = intervention.get("weight", 1.0)

        raw = effectiveness_history.get(iid, 0.5)

        # ⭐ FIX: If effectiveness is a list, convert to average
        if isinstance(raw, list):
            effectiveness = sum(raw) / len(raw)
        else:
            effectiveness = raw

        # Update rule: move weight toward effectiveness
        delta = (effectiveness - 0.5) * learning_rate
        new_weight = max(0.0, weight + delta)

        updated.append({
            **intervention,
            "weight": round(new_weight, 3)
        })

    return updated


def select_intervention(interventions: List[Dict]):
    """
    Selects the intervention with the highest weight.
    """

    if not interventions:
        return None

    return max(interventions, key=lambda x: x.get("weight", 0.0))


def optimize(interventions: List[Dict], effectiveness_history: Dict[str, float]):
    """
    Full optimization pipeline:
    - update weights based on effectiveness
    - select best intervention
    """

    updated = update_intervention_weights(interventions, effectiveness_history)
    best = select_intervention(updated)

    return {
        "updated_interventions": updated,
        "selected_intervention": best,
    }
