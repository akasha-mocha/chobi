from pathlib import Path
from typing import Dict
import subprocess
import time

from scripts.utils.logger import get_logger
from scripts.ai.ai_runner import run_ai

logger = get_logger("task_engine")

ROOT = Path(__file__).resolve().parents[2]

TASK_DIR = ROOT / "tickets/tasks"
BUG_DIR = ROOT / "tickets/bugs"


class TaskExecutionEngine:

    def __init__(self):

        self.task_dir = TASK_DIR
        self.bug_dir = BUG_DIR

    # -----------------------------

    def list_tasks(self):

        if not self.task_dir.exists():
            return []

        return list(self.task_dir.glob("*.md"))

    # -----------------------------

    def read_task(self, path: Path):

        with open(path, encoding="utf8") as f:
            return f.read()

    # -----------------------------

    def mark_task_done(self, path: Path):

        text = self.read_task(path)

        text = text.replace(
            "Status: OPEN",
            "Status: DONE"
        )

        with open(path, "w", encoding="utf8") as f:
            f.write(text)

    # -----------------------------

    def create_bug(self, task_path: Path, error: str):

        bug_id = int(time.time())

        bug_file = self.bug_dir / f"bug_{bug_id}.md"

        text = f"""
ID: BUG-{bug_id}
Title: Task execution failed
Status: OPEN
Priority: HIGH
Task: {task_path.name}

Error:
{error}
"""

        bug_file.parent.mkdir(parents=True, exist_ok=True)

        with open(bug_file, "w", encoding="utf8") as f:
            f.write(text)

        logger.warning(f"Bug created: {bug_file}")

    # -----------------------------

    def generate_code(self, task_text: str):

        prompt = f"""
You are a senior software engineer.

Implement the following task.

{task_text}
"""

        result = run_ai(prompt)

        return result

    # -----------------------------

    def run_tests(self):

        try:

            result = subprocess.run(
                ["pytest"],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:

                return False, result.stdout + result.stderr

            return True, ""

        except Exception as e:

            return False, str(e)

    # -----------------------------

    def execute_task(self, task_path: Path):

        logger.info(f"Executing task {task_path}")

        task_text = self.read_task(task_path)

        try:

            code = self.generate_code(task_text)

            logger.info("AI generated code")

        except Exception as e:

            logger.error(str(e))

            self.create_bug(task_path, str(e))

            return

        ok, error = self.run_tests()

        if not ok:

            self.create_bug(task_path, error)

            return

        self.mark_task_done(task_path)

        logger.info("Task completed")

    # -----------------------------

    def run_next_task(self):

        tasks = self.list_tasks()

        if not tasks:

            logger.info("No tasks available")

            return

        task = tasks[0]

        self.execute_task(task)