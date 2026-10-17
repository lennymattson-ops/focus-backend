# ---------------------------------------------------------
# Behavioral State Engine (Phase 3)
# ---------------------------------------------------------
# This engine converts daily check‑in inputs into a unified
# behavioral state profile aligned with the architecture docs.
# ---------------------------------------------------------

def normalize_input(value, min_val=0, max_val=10):
    """
    Normalize check‑in values (0–10) into a 0–1 scale.
    Ensures numeric input and clamps to valid range.
    """
    try:
        value = float(value)
    except:
        return 0.0

    value = max(min(value, max_val), min_val)
    return round(value / max_val, 3)


def compute_risk(motivation, energy, consistency):
    """
    Simple risk model:
    Lower motivation, energy, or consistency increases risk.
    Risk is returned on a 0–1 scale.
    """
    avg = (motivation + energy + consistency) / 3
    risk = 1 - avg
    return round(risk, 3)


def extract_flags(state):
    """
    Pattern identification and behavioral indicators.
    These flags help the decision engine understand conditions.
    """
    return {
        "low_motivation": state["motivation"] < 0.3,
        "low_energy": state["energy"] < 0.3,
        "inconsistent": state["consistency"] < 0.3,
        "high_risk": state["risk"] > 0.7
    }


def build_behavioral_state(data):
    """
    Build a unified behavioral state profile from daily check‑in inputs.
    Inputs expected from the Daily Check‑In Page:
        motivation (0–10)
        energy (0–10)
        consistency (0–10)
        risk (optional — auto‑computed if not provided)
    """

    motivation = normalize_input(data.get("motivation", 5))
    energy = normalize_input(data.get("energy", 5))
    consistency = normalize_input(data.get("consistency", 5))

    # If risk is provided manually, normalize it.
    # Otherwise compute it automatically.
    if "risk" in data:
        risk = normalize_input(data.get("risk", 5))
    else:
        risk = compute_risk(motivation, energy, consistency)

    state = {
        "motivation": motivation,
        "energy": energy,
        "consistency": consistency,
        "risk": risk
    }

    # Add pattern flags
    state["flags"] = extract_flags(state)

    return state


def process(state_input: dict):
    """
    Public API used by /state endpoint.
    Converts raw check‑in input into a behavioral state.
    """
    return build_behavioral_state(state_input)

