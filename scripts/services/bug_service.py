import json
import os
from datetime import datetime

BUG_DIR = "tickets/bugs"


def list_bugs():
    bugs = []

    if not os.path.exists(BUG_DIR):
        return bugs

    for f in os.listdir(BUG_DIR):
        if f.endswith(".json"):
            with open(os.path.join(BUG_DIR, f), "r", encoding="utf-8") as fp:
                bugs.append(json.load(fp))

    return bugs


def create_bug(task_id, description, error_log=None):
    os.makedirs(BUG_DIR, exist_ok=True)

    bug_id = f"bug_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    bug = {
        "id": bug_id,
        "task_id": task_id,
        "description": description,
        "error_log": error_log,
        "status": "open",
        "created": datetime.now().isoformat()
    }

    path = os.path.join(BUG_DIR, f"{bug_id}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(bug, f, indent=2, ensure_ascii=False)

    return bug


def close_bug(bug_id):
    path = os.path.join(BUG_DIR, f"{bug_id}.json")

    if not os.path.exists(path):
        raise Exception("Bug not found")

    with open(path, "r", encoding="utf-8") as f:
        bug = json.load(f)

    bug["status"] = "closed"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(bug, f, indent=2, ensure_ascii=False)

    return bug