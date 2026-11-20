"""Turn English check-in text into draft slider values, without saving it."""

import re

MAX_TEXT_LENGTH = 4000

# Each rule groups phrases that point to the same score direction.
# The scores are starting guesses on the existing 0–10 slider scale.
RULES = {
    "motivation": {
        2: (
            "i feel unmotivated", "i'm unmotivated", "i am unmotivated",
            "i have no motivation", "i'm not motivated", "i am not motivated",
            "i can't bring myself to start",
        ),
        8: (
            "i feel motivated", "i'm motivated", "i am motivated",
            "i'm excited to", "i am excited to", "i'm excited about",
            "i am excited about", "i'm eager to", "i am eager to",
        ),
    },
    "energy": {
        2: (
            "i'm exhausted", "i am exhausted", "i feel exhausted", "i'm tired",
            "i am tired", "i feel tired", "i barely slept", "barely slept",
            "i have no energy", "i feel drained",
        ),
        8: (
            "i slept well", "i feel rested", "i'm well rested",
            "i feel energized", "i'm energized", "i have plenty of energy",
        ),
    },
    "consistency": {
        2: (
            "i keep putting it off", "i keep starting things and dropping them",
            "i haven't been sticking to my routine", "i keep skipping",
            "i keep procrastinating", "i haven't been consistent",
        ),
        8: (
            "i've been consistent", "i've stuck to my routine",
            "i've been sticking to my routine", "i've stayed on track",
            "i've been following through",
        ),
    },
    # "Risk" is the prototype's stress/risk slider, not a safety assessment.
    "risk": {
        2: (
            "i feel calm", "i'm calm", "i am calm", "i'm not stressed",
            "i am not stressed", "i feel relaxed",
        ),
        8: (
            "i feel overwhelmed", "i'm overwhelmed", "i am overwhelmed",
            "i feel stressed", "i'm stressed", "i am stressed",
            "i feel under pressure",
        ),
    },
}

# Compile once, and match complete phrases rather than fragments of words.
PATTERNS = {
    dimension: {
        score: re.compile(r"\b(?:" + "|".join(map(re.escape, phrases)) + r")\b")
        for score, phrases in groups.items()
    }
    for dimension, groups in RULES.items()
}


def parse_checkin(text: str) -> dict:
    """Return reviewable suggestions in a format independent of the API."""
    normalized = " ".join(text.lower().replace("’", "'").replace("‘", "'").split())
    scores = {}
    evidence = {}
    status = {}

    for dimension, groups in PATTERNS.items():
        matches = []
        for score, pattern in groups.items():
            for match in pattern.finditer(normalized):
                # A bare "barely slept" is supported as a stand-alone note,
                # not when it might describe somebody else in a sentence.
                if match[0] == "barely slept" and normalized.rstrip(".!?") != match[0]:
                    continue
                matches.append((match.start(), match[0], score))
        matches.sort()
        evidence[dimension] = list(dict.fromkeys(phrase for _, phrase, _ in matches))
        candidates = {score for _, _, score in matches}

        # Don't average contradictory clues or fill in unmentioned values.
        scores[dimension] = next(iter(candidates)) if len(candidates) == 1 else None
        status[dimension] = (
            "suggested" if len(candidates) == 1
            else "conflicting" if candidates
            else "unknown"
        )

    return {
        "parser_version": "rules-v1",
        "scores": scores,
        "status": status,
        "evidence": evidence,
        "requires_review": True,
    }
