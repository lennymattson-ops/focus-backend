def analyze_behavioral_state(state):
    """
    Analyzes the behavioral state and identifies risks + opportunities.
    """

    motivation = state["motivation"]
    energy = state["energy"]
    consistency = state["consistency"]
    risk = state["risk"]

    risks = []
    opportunities = []

    # Risk detection
    if motivation < 40:
        risks.append("Low motivation")
    if energy < 40:
        risks.append("Low energy")
    if consistency < 40:
        risks.append("Low consistency")
    if risk > 60:
        risks.append("High burnout / regression risk")

    # Opportunity detection
    if motivation > 70:
        opportunities.append("Strong motivation — good time to push goals")
    if consistency > 70:
        opportunities.append("High consistency — reinforce habits")
    if energy > 70:
        opportunities.append("High energy — schedule demanding tasks")

    return {
        "risks": risks,
        "opportunities": opportunities
    }


def generate_intervention(analysis):
    """
    Generates a simple intervention based on detected risks/opportunities.
    """

    risks = analysis["risks"]
    opportunities = analysis["opportunities"]

    # Priority: address risks first
    if "High burnout / regression risk" in risks:
        return "Take a recovery day. Reduce workload. Hydrate. Light movement only."

    if "Low motivation" in risks:
        return "Write a 2-minute reflection: Why does your goal matter today?"

    if "Low consistency" in risks:
        return "Set a tiny habit for today: something you can finish in under 3 minutes."

    if "Low energy" in risks:
        return "Take a 10-minute walk or stretch session to reset your energy."

    # If no risks, use opportunities
    if "Strong motivation — good time to push goals" in opportunities:
        return "Choose one important task and commit to finishing it today."

    if "High consistency — reinforce habits" in opportunities:
        return "Increase your habit difficulty slightly — you're ready."

    if "High energy — schedule demanding tasks" in opportunities:
        return "Schedule your most difficult task in the next 2 hours."

    # Default fallback
    return "Everything looks stable. Maintain your current routine."
