from scripts.ai.generation.code_generator import generate_code
from scripts.services.task_service import update_task


def execute_task(task):

    print("Executing task:", task["title"])

    result = generate_code(task)

    if result:
        update_task(task["id"], "generated")

    return result