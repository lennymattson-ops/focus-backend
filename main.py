# ---------------------------------------------------------
# Closed Loop Engine + Behavioral Memory Append
# ---------------------------------------------------------
@app.post("/loop")
def loop_endpoint(data: dict):
    previous_state = data.get("previous_state", {})
    current_state = data.get("current_state", {})
    decision = data.get("decision", {})
    outcome = data.get("outcome", {})
    interventions = data.get("interventions", [])
    effectiveness_history = data.get("effectiveness_history", {})
    selected_intervention = data.get("selected_intervention", {})
    completed = data.get("completed", False)

    # Run closed loop engine
    loop_result = closed_loop(
        previous_state,
        current_state,
        decision,
        outcome,
        interventions,
        effectiveness_history,
        selected_intervention,
        completed,
    )

    # Build daily history record
    record = {
        "timestamp": datetime.now().isoformat(),
        "previous_state": previous_state,
        "current_state": current_state,
        "decision": decision,
        "outcome": outcome,

        # Store intervention data directly
        "selected_intervention": selected_intervention,
        "updated_interventions": interventions,

        "effectiveness_history": effectiveness_history,

        "loop_result": loop_result,
    }

    append_record(record)

    return loop_result
