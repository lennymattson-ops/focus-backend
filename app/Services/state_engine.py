# ---------------------------------------------------------
# Behavioral State Engine (Phase 3.1)
# ---------------------------------------------------------
# This engine converts daily check-in inputs into a unified
# behavioral state profile aligned with the architecture docs.
#
# Fixes:
# - Prevents state values from exceeding 1.0
# - Prevents state values from dropping below 0.0
# - Guarantees risk stays in valid range
# - Defensive protection against future engine changes
# ---------------------------------------------------------


def normalize_input(value, min_val=0, max_val=10):
    """
    Normalize check-in values (0–10) into a 0–1 scale.
    Ensures numeric input and clamps to valid range.
    """
    try:
        value = float(value)
    except Exception:
        return 0.0

    value = max(min(value, max_val), min_val)

    return round(value / max_val, 3)


def clamp_state_value(value):
    """
    Ensure all behavioral state values remain
    between 0.0 and 1.0.
    """

    try:
        value = float(value)
    except Exception:
        return 0.0

    return round(
        max(
            0.0,
            min(value, 1.0)
        ),
        3
    )


def compute_risk(
    motivation,
    energy,
    consistency
):
    """
    Simple risk model:

    Lower motivation, energy, or consistency
    increases risk.

    Risk is returned on a 0–1 scale.
    """

    avg = (
        motivation
        + energy
        + consistency
    ) / 3

    risk = 1 - avg

    return clamp_state_value(risk)


def extract_flags(state):
    """
    Pattern identification and behavioral indicators.

    These flags help the decision engine
    understand conditions.
    """

    return {
        "low_motivation":
            state["motivation"] < 0.3,

        "low_energy":
            state["energy"] < 0.3,

        "inconsistent":
            state["consistency"] < 0.3,

        "high_risk":
            state["risk"] > 0.7,
    }


def build_behavioral_state(data):
    """
    Build a unified behavioral state profile
    from daily check-in inputs.

    Inputs expected:

        motivation (0–10)

        energy (0–10)

        consistency (0–10)

        risk (optional)
    """

    motivation = normalize_input(
        data.get("motivation", 5)
    )

    energy = normalize_input(
        data.get("energy", 5)
    )

    consistency = normalize_input(
        data.get("consistency", 5)
    )

    # If risk is supplied manually,
    # normalize it.
    if "risk" in data:

        risk = normalize_input(
            data.get("risk", 5)
        )

    else:

        risk = compute_risk(
            motivation,
            energy,
            consistency
        )

    # HARD CLAMP ALL VALUES
    # This prevents issues like:
    #
    # risk = 2
    # motivation = -1
    #
    # from ever appearing in history.
    state = {
        "motivation":
            clamp_state_value(
                motivation
            ),

        "energy":
            clamp_state_value(
                energy
            ),

        "consistency":
            clamp_state_value(
                consistency
            ),

        "risk":
            clamp_state_value(
                risk
            )
    }

    state["flags"] = extract_flags(
        state
    )

    return state


def process(state_input: dict):
    """
    Public API used by /state endpoint.

    Converts raw check-in input into a
    behavioral state profile.
    """

    return build_behavioral_state(
        state_input
    )