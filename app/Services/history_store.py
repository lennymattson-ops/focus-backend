import json
from typing import List, Dict
from pathlib import Path

HISTORY_FILE = Path(__file__).parent.parent / "behavior_history.json"


def load_history() -> List[Dict]:
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def append_record(record: Dict):
    history = load_history()
    history.append(record)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)
