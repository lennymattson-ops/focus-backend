from typing import List, Dict


def update_intervention_weights(
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    learning_rate: float = 0.1,
):
    """
    Adjusts intervention weights based on historical effectiveness.

    interventions: list of { "id": str, "name": str, "weight": float }
    effectiveness_history: { intervention_id: effectiveness_score }
    """

    updated = []

    for intervention in interventions:
        iid = intervention["id"]
        weight = intervention.get("weight", 1.0)
        effectiveness = effectiveness_history.get(iid, 0.5)  # default neutral

        # Simple update rule:
        # - if effectiveness > 0.5 → increase weight
        # - if effectiveness < 0.5 → decrease weight
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
