from app.Services.decision_engine import process_decision
from app.Services.outcome_engine import process_outcome
from app.Services.optimization_engine import optimize


def closed_loop(previous_state, current_state, interventions, effectiveness_history, completed):
    """
    Full closed-loop behavioral optimization cycle.
    """

    # 1. Generate decision (intervention)
    decision = process_decision(previous_state)

    # 2. Measure outcome
    outcome_data = {
        "previous_state": previous_state,
        "current_state": current_state,
        "completed": completed
    }
    outcome = process_outcome(outcome_data)

    # 3. Update effectiveness history
    # Use numeric_score as effectiveness
    effectiveness_history[decision["recommended_intervention"]] = outcome["numeric_score"]

    # 4. Optimize intervention weights
    optimization_result = optimize(interventions, effectiveness_history)

    return {
        "decision": decision,
        "outcome": outcome,
        "optimization": optimization_result
    }
