import json
import os

HISTORY_FILE = "behavior_history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def append_record(record):
    history = load_history()
    history.append(record)
    save_history(history)
    return record
