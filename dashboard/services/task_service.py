import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TASK_DIR = ROOT / "tickets/tasks"


def parse_task_md(text: str):

    task = {
        "id": "",
        "title": "Untitled Task",
        "status": "unknown",
        "priority": ""
    }

    id_match = re.search(r"^ID:\s*(.*)", text, re.MULTILINE)
    if id_match:
        task["id"] = id_match.group(1).strip()

    title_match = re.search(r"^Title:\s*(.*)", text, re.MULTILINE)
    if title_match:
        value = title_match.group(1).strip()
        if value:
            task["title"] = value

    status_match = re.search(r"^Status:\s*(.*)", text, re.MULTILINE)
    if status_match:
        value = status_match.group(1).strip()
        if value:
            task["status"] = value

    priority_match = re.search(r"^Priority:\s*(.*)", text, re.MULTILINE)
    if priority_match:
        task["priority"] = priority_match.group(1).strip()

    return task


def get_tasks():

    tasks = []

    if not TASK_DIR.exists():
        return tasks

    for f in TASK_DIR.glob("*.md"):

        try:

            with open(f, encoding="utf8") as fp:
                text = fp.read()

            task = parse_task_md(text)

            tasks.append(task)

        except Exception:
            continue

    return tasks