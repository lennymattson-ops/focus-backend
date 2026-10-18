from typing import Dict, List


def closed_loop(
    previous_state: Dict,
    current_state: Dict,
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    completed: bool
):
    """
    Phase 9 Closed Loop Engine:
    - Computes state shift
    - Computes intervention effectiveness
    - Returns loop result for history, dashboard, and optimizer.
    """

    # Compute state shift between previous and current state
    state_shift = {
        "motivation_change": current_state.get("motivation", 0) - previous_state.get("motivation", 0),
        "energy_change": current_state.get("energy", 0) - previous_state.get("energy", 0),
        "consistency_change": current_state.get("consistency", 0) - previous_state.get("consistency", 0),
        "risk_change": current_state.get("risk", 0) - previous_state.get("risk", 0),
    }

    # Simple effectiveness score (Phase 10 can replace this)
    effectiveness_score = (
        state_shift["motivation_change"] +
        state_shift["energy_change"] +
        state_shift["consistency_change"] -
        state_shift["risk_change"]
    )

    loop_result = {
        "state_shift": state_shift,
        "intervention_effectiveness": round(effectiveness_score, 3),

        # Phase 9: pass through learning context for optimizer
        "effectiveness_history": effectiveness_history,
        "interventions": interventions,

        "completed": completed
    }

    return loop_result
