import re
from pathlib import Path

from dashboard.services.cache_utils import TimedCache

ROOT = Path(__file__).resolve().parents[2]
TASK_DIR = ROOT / "tickets/tasks"

_cache = TimedCache(ttl=3)


def parse_task_md(text: str):

    task = {
        "id": "",
        "title": "",
        "status": "",
        "priority": ""
    }

    id_match = re.search(r"^ID:\s*(.*)", text, re.MULTILINE | re.IGNORECASE)
    if id_match:
        task["id"] = id_match.group(1).strip()

    title_match = re.search(r"^Title:\s*(.*)", text, re.MULTILINE | re.IGNORECASE)
    if title_match:
        task["title"] = title_match.group(1).strip()

    status_match = re.search(r"^Status:\s*(.*)", text, re.MULTILINE | re.IGNORECASE)
    if status_match:
        task["status"] = status_match.group(1).strip()

    priority_match = re.search(r"^Priority:\s*(.*)", text, re.MULTILINE | re.IGNORECASE)
    if priority_match:
        task["priority"] = priority_match.group(1).strip()

    return task


def _load_tasks():

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


def get_tasks():
    return _cache.get(_load_tasks)