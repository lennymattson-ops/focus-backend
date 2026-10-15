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

def process(state_input: dict):
    text = state_input.get("yourInput", "").lower()

    # Simple feature extraction
    length = len(text)
    has_negative_words = any(w in text for w in ["tired", "stuck", "overwhelmed", "behind"])
    has_positive_words = any(w in text for w in ["motivated", "excited", "ready", "focused"])

    # Basic classification
    motivation_level = "medium"
    if has_positive_words:
        motivation_level = "high"
    if has_negative_words:
        motivation_level = "low"

    consistency_level = "unknown"
    engagement_level = "unknown"

    # Generate behavioral state
    behavioral_state = {
        "motivation_level": motivation_level,
        "engagement_level": engagement_level,
        "consistency_level": consistency_level,
        "input_length": length,
        "raw_input": text
    }

    return behavioral_state
