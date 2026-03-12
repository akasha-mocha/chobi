import os
import json

TASK_DIR = "tickets/tasks"


def load_task(path):

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_open_tasks():

    tasks = []

    if not os.path.exists(TASK_DIR):
        return tasks

    for file in os.listdir(TASK_DIR):

        if file.endswith(".json"):

            task = load_task(os.path.join(TASK_DIR, file))

            if task.get("status") == "open":

                task["file"] = os.path.join(TASK_DIR, file)

                tasks.append(task)

    return tasks


def save_task(task):

    with open(task["file"], "w", encoding="utf-8") as f:

        json.dump(task, f, indent=2)


def mark_done(task_id):

    tasks = get_open_tasks()

    for t in tasks:

        if t["id"] == task_id:

            t["status"] = "done"

            save_task(t)


def mark_failed(task_id):

    tasks = get_open_tasks()

    for t in tasks:

        if t["id"] == task_id:

            t["status"] = "failed"

            save_task(t)