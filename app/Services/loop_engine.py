from typing import Dict, List


def closed_loop(
    previous_state: Dict,
    current_state: Dict,
    decision: Dict,
    outcome: Dict,
    interventions: List[Dict],
    effectiveness_history: Dict[str, float],
    selected_intervention: Dict,
    completed: bool
):
    """
    Phase 10 Closed Loop Engine

    Responsibilities:
    - Compute state shift
    - Compute intervention effectiveness
    - Update effectiveness history
    - Return synchronized loop result
    """

    # --------------------------------------------------
    # State Shift
    # --------------------------------------------------

    state_shift = {
        "motivation_change":
            current_state.get("motivation", 0)
            - previous_state.get("motivation", 0),

        "energy_change":
            current_state.get("energy", 0)
            - previous_state.get("energy", 0),

        "consistency_change":
            current_state.get("consistency", 0)
            - previous_state.get("consistency", 0),

        "risk_change":
            current_state.get("risk", 0)
            - previous_state.get("risk", 0),
    }

    # --------------------------------------------------
    # Intervention Effectiveness
    # --------------------------------------------------

    effectiveness_score = (
        state_shift["motivation_change"]
        + state_shift["energy_change"]
        + state_shift["consistency_change"]
        - state_shift["risk_change"]
    )

    effectiveness_score = round(
        effectiveness_score,
        3
    )

    # --------------------------------------------------
    # Synchronize Effectiveness History
    # --------------------------------------------------

    updated_effectiveness_history = {
        "overall": effectiveness_score,
        "selected_intervention":
            selected_intervention.get(
                "name",
                None
            )
    }

    # --------------------------------------------------
    # Loop Result
    # --------------------------------------------------

    loop_result = {
        "state_shift": state_shift,

        "intervention_effectiveness":
            effectiveness_score,

        "decision": decision,

        "outcome": outcome,

        "interventions":
            interventions,

        "effectiveness_history":
            updated_effectiveness_history,

        "selected_intervention":
            selected_intervention,

        "completed":
            completed
    }

    return loop_result
