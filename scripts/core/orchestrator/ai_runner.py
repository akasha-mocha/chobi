from scripts.core.engine.dev_cycle import run_dev_cycle
from scripts.services.task_service import list_tasks


def run_ai_dev():

    print("=== AI DEV START ===")

    tasks = list_tasks()

    if not tasks:
        print("No tasks found")
        return

    for task in tasks:
        print(f"Processing task: {task['title']}")
        run_dev_cycle(task)

    print("=== AI DEV END ===")