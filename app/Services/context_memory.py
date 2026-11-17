import json
from pathlib import Path

# Anchor to the app directory (like history_store) so the file
# location does not depend on the working directory uvicorn
# was launched from
CONTEXT_MEMORY_FILE = Path(__file__).parent.parent / "context_memory.json"
MAX_HISTORY_PER_CONTEXT = 20


def load_context_memory():
    """
    Load contextual learning memory.

    Returns:
        dict
    """

    if not CONTEXT_MEMORY_FILE.exists():
        return {}

    try:

        with open(
            CONTEXT_MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:
        return {}


def save_context_memory(memory):
    """
    Save contextual learning memory.
    """

    print(
        "CONTEXT MEMORY PATH:",
        CONTEXT_MEMORY_FILE.resolve()
    )

    with open(
        CONTEXT_MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            memory,
            f,
            indent=4
        )


def record_context_outcome(
    risks,
    intervention_name,
    effectiveness_score
):
    """
    Stores intervention outcomes
    inside context memory.

    Example:

    Low energy
        -> Energy Reset
            -> [1.2, 0.8]

    High risk
        -> Risk Reduction
            -> [1.0, 1.4]
    """

    print(
        "RECORD_CONTEXT_OUTCOME CALLED:",
        risks,
        intervention_name,
        effectiveness_score
    )

    memory = load_context_memory()

    for risk in risks:

        if risk not in memory:
            memory[risk] = {}

        if intervention_name not in memory[risk]:
            memory[risk][intervention_name] = []

        memory[risk][intervention_name].append(
            effectiveness_score
        )

        memory[risk][intervention_name] = (
            memory[risk][intervention_name][
                -MAX_HISTORY_PER_CONTEXT:
            ]
        )

    save_context_memory(memory)

def get_context_learning_score(
    risks,
    intervention_name
):
    """
    Returns average contextual
    effectiveness across all
    active risks.
    """

    if not risks:
        return 0

    scores = []

    for risk in risks:

        score = get_context_score(
            risk,
            intervention_name
        )

        if score != 0:
            scores.append(score)

    if not scores:
        return 0

    return sum(scores) / len(scores) 

def get_context_score(
    risk,
    intervention_name
):
    """
    Returns average effectiveness
    for an intervention within a context.

    Example:

    Low energy
        -> Energy Reset
            -> [1.2, 0.8]

    returns:

    1.0
    """

    memory = load_context_memory()

    if risk not in memory:
        return 0

    if intervention_name not in memory[risk]:
        return 0

    history = memory[risk][intervention_name]

    if not history:
        return 0

    return sum(history) / len(history)