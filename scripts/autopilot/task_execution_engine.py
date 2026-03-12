from pathlib import Path

from scripts.autopilot.ticket_state_manager import set_task_doing, set_task_done
from scripts.ai.ai_executor import run_ai_task
from scripts.utils.logger import get_logger

ROOT = Path(__file__).resolve().parents[2]

TASK_DIR = ROOT / "tickets/tasks"

logger = get_logger("task_engine")


def find_next_task():

    for f in TASK_DIR.glob("*.md"):

        text = f.read_text()

        if "Status: todo" in text:
            return f

    return None


def run_next_task():

    task_file = find_next_task()

    if not task_file:
        return

    logger.info(f"run task {task_file.name}")

    set_task_doing(task_file)

    run_ai_task(task_file)

    set_task_done(task_file)