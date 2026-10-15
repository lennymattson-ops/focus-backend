def analyze_behavioral_state(state):
    """
    Analyze the behavioral state and identify risks + opportunities.
    """

    motivation = state.get("motivation_level", "medium")
    length = state.get("input_length", 0)

    risks = []
    opportunities = []

    # Risk detection
    if motivation == "low":
        risks.append("Low motivation")
    if length < 10:
        risks.append("Low engagement")

    # Opportunity detection
    if motivation == "high":
        opportunities.append("Strong motivation — good time to push goals")
    if length > 50:
        opportunities.append("High engagement — user is expressive")

    return {
        "risks": risks,
        "opportunities": opportunities
    }


def generate_intervention(analysis):
    """
    Generate an intervention based on detected risks/opportunities.
    """

    risks = analysis["risks"]
    opportunities = analysis["opportunities"]

    # Priority: address risks first
    if "Low motivation" in risks:
        return "Write a 2-minute reflection: Why does your goal matter today?"

    if "Low engagement" in risks:
        return "Set a tiny habit for today: something you can finish in under 3 minutes."

    # If no risks, use opportunities
    if "Strong motivation — good time to push goals" in opportunities:
        return "Choose one important task and commit to finishing it today."

    if "High engagement — user is expressive" in opportunities:
        return "Increase your habit difficulty slightly — you're ready."

    # Default fallback
    return "Everything looks stable. Maintain your current routine."


def process_decision(state):
    """
    Full decision engine pipeline:
    - analyze behavioral state
    - generate intervention
    """

    analysis = analyze_behavioral_state(state)
    intervention = generate_intervention(analysis)

    return {
        "analysis": analysis,
        "recommended_intervention": intervention
    }
