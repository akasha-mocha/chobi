from dashboard.services.task_service import get_tasks
from dashboard.services.bug_service import get_bugs


def get_metrics():

    tasks = get_tasks()
    bugs = get_bugs()

    return {
        "tasks": len(tasks),
        "bugs": len(bugs)
    }