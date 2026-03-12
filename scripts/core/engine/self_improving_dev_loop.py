from scripts.core.orchestrator.task_executor import execute_task
from scripts.core.orchestrator.test_executor import execute_tests
from scripts.core.orchestrator.bug_executor import process_test_result

from scripts.services.bug_service import list_bugs
from scripts.ai.generation.code_generator import generate_code
from scripts.ai.evaluation.bug_detector import detect_bug

MAX_FIX_ATTEMPTS = 3


def run_self_improving_loop(task):

    print("=== SELF IMPROVING LOOP ===")
    print("Task:", task["title"])

    # 1 Code Generation
    execute_task(task)

    attempts = 0

    while attempts < MAX_FIX_ATTEMPTS:

        print("Running tests...")

        # 2 Run Tests
        test_result = execute_tests()

        # 3 If success → done
        if test_result["success"]:
            print("Task completed successfully")
            return True

        print("Test failed. Detecting bug...")

        # 4 Bug Detection
        bug_info = detect_bug(test_result)

        # 5 Bug Ticket
        process_test_result(task, test_result)

        print("Generating fix...")

        # 6 Fix Generation
        generate_fix(task, bug_info)

        attempts += 1

    print("Max fix attempts reached")

    return False


def generate_fix(task, bug_info):

    fix_prompt = {
        "task": task,
        "bug": bug_info
    }

    generate_code(fix_prompt)