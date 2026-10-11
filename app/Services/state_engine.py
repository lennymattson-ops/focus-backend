def normalize_input(value, min_val=0, max_val=100):
    """
    Ensures all inputs are between 0–100.
    Converts non-numeric values to 0.
    """
    try:
        value = float(value)
    except:
        return 0

    return max(min(value, max_val), min_val)


def build_behavioral_state(data):
    """
    Builds a behavioral state object from normalized inputs.
    """

    motivation = normalize_input(data.get("motivation", 50))
    energy = normalize_input(data.get("energy", 50))
    consistency = normalize_input(data.get("consistency", 50))
    tasks_completed = normalize_input(data.get("tasks_completed", 0))
    sleep_quality = normalize_input(data.get("sleep_quality", 50))

    # Simple risk model (we will improve this later)
    risk = 100 - ((motivation + consistency + energy) / 3)

    return {
        "motivation": motivation,
        "energy": energy,
        "consistency": consistency,
        "tasks_completed": tasks_completed,
        "sleep_quality": sleep_quality,
        "risk": round(risk, 2)
    }
