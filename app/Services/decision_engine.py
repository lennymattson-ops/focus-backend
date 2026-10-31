def analyze_behavioral_state(state):
    """
    Analyze behavioral state and generate
    dynamic risks/opportunities from actual metrics.
    """

    motivation = state.get("motivation", 0.5)
    energy = state.get("energy", 0.5)
    consistency = state.get("consistency", 0.5)
    risk = state.get("risk", 0.5)

    risks = []
    opportunities = []

    # --------------------------
    # Risk Detection
    # --------------------------

    if motivation < 0.3:
        risks.append("Low motivation")

    if energy < 0.3:
        risks.append("Low energy")

    if consistency < 0.3:
        risks.append("Inconsistent behavior")

    if risk > 0.7:
        risks.append("High risk")

    # --------------------------
    # Opportunity Detection
    # --------------------------

    if motivation > 0.7:
        opportunities.append(
            "High motivation available"
        )

    if energy > 0.7:
        opportunities.append(
            "High energy available"
        )

    if consistency > 0.7:
        opportunities.append(
            "Strong consistency trend"
        )

    if risk < 0.3:
        opportunities.append(
            "Low risk environment"
        )

    return {
        "risks": risks,
        "opportunities": opportunities
    }


def generate_intervention(analysis):
    """
    Select intervention based on highest-priority risk.
    """

    risks = analysis["risks"]
    opportunities = analysis["opportunities"]

    if "High risk" in risks:
        return (
            "Reduce friction. Remove one obstacle "
            "or distraction before starting work."
        )

    if "Low energy" in risks:
        return (
            "Take a short reset: hydration, movement, "
            "or a 5-minute break."
        )

    if "Low motivation" in risks:
        return (
            "Write a short reminder of why your goal "
            "matters today."
        )

    if "Inconsistent behavior" in risks:
        return (
            "Choose a tiny habit you can complete "
            "in under 3 minutes."
        )

    if "High motivation available" in opportunities:
        return (
            "Use your momentum. Choose one meaningful "
            "task and finish it today."
        )

    if "High energy available" in opportunities:
        return (
            "Tackle a challenging task while energy "
            "is elevated."
        )

    if "Strong consistency trend" in opportunities:
        return (
            "Increase your habit difficulty slightly."
        )

    if "Low risk environment" in opportunities:
        return (
            "This is a good time to pursue a larger goal."
        )

    return (
        "Everything looks stable. Maintain your "
        "current routine."
    )


def process_decision(state):
    """
    Full decision engine pipeline.
    """

    analysis = analyze_behavioral_state(state)

    intervention = generate_intervention(
        analysis
    )

    return {
        "analysis": analysis,
        "recommended_intervention": intervention,
    }