import json
import os
from datetime import datetime

TASK_DIR = "tickets/tasks"


def list_tasks():
    tasks = []
    if not os.path.exists(TASK_DIR):
        return tasks

    for f in os.listdir(TASK_DIR):
        if f.endswith(".json"):
            with open(os.path.join(TASK_DIR, f), "r", encoding="utf-8") as fp:
                tasks.append(json.load(fp))
    return tasks


def create_task(title, description):
    os.makedirs(TASK_DIR, exist_ok=True)

    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "status": "open",
        "created": datetime.now().isoformat()
    }

    path = os.path.join(TASK_DIR, f"{task_id}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(task, f, indent=2, ensure_ascii=False)

    return task


def update_task(task_id, status):
    path = os.path.join(TASK_DIR, f"{task_id}.json")

    if not os.path.exists(path):
        raise Exception("Task not found")

    with open(path, "r", encoding="utf-8") as f:
        task = json.load(f)

    task["status"] = status

    with open(path, "w", encoding="utf-8") as f:
        json.dump(task, f, indent=2, ensure_ascii=False)

    return task