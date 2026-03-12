import time
import traceback
from pathlib import Path
from typing import List

from scripts.utils.logger import get_logger

logger = get_logger("task_engine")

ROOT = Path(__file__).resolve().parents[2]

TASK_DIR = ROOT / "tickets/tasks"
BUG_DIR = ROOT / "tickets/bugs"

AUTOPILOT_STATE = ROOT / "runtime/autopilot_state.txt"


class Task:

    def __init__(self, file: Path):

        self.file = file
        self.id = ""
        self.title = ""
        self.status = ""
        self.priority = ""

        self._parse()

    def _parse(self):

        text = self.file.read_text(encoding="utf8")

        for line in text.splitlines():

            if line.startswith("ID:"):
                self.id = line.split(":", 1)[1].strip()

            if line.startswith("Title:"):
                self.title = line.split(":", 1)[1].strip()

            if line.startswith("Status:"):
                self.status = line.split(":", 1)[1].strip()

            if line.startswith("Priority:"):
                self.priority = line.split(":", 1)[1].strip()

    def set_status(self, new_status: str):

        text = self.file.read_text(encoding="utf8")

        lines = []

        for line in text.splitlines():

            if line.startswith("Status:"):
                lines.append(f"Status: {new_status}")
            else:
                lines.append(line)

        self.file.write_text("\n".join(lines), encoding="utf8")


class TaskExecutionEngine:

    def __init__(self):

        logger.info("TaskExecutionEngine initialized")

    # --------------------------------
    # autopilot state
    # --------------------------------

    def autopilot_state(self):

        if not AUTOPILOT_STATE.exists():
            return "STOP"

        return AUTOPILOT_STATE.read_text().strip()

    # --------------------------------
    # load tasks
    # --------------------------------

    def load_tasks(self) -> List[Task]:

        tasks = []

        if not TASK_DIR.exists():
            return tasks

        for f in TASK_DIR.glob("*.md"):

            try:

                task = Task(f)

                if task.status.upper() == "OPEN":
                    tasks.append(task)

            except Exception as e:

                logger.error(f"Task parse error {f}: {e}")

        return tasks

    # --------------------------------
    # AI execution stub
    # --------------------------------

    def execute_task(self, task: Task):

        logger.info(f"Executing task {task.id} : {task.title}")

        # TODO: AI execution here

        time.sleep(2)

        return True

    # --------------------------------
    # bug create
    # --------------------------------

    def create_bug(self, task: Task, error: str):

        BUG_DIR.mkdir(parents=True, exist_ok=True)

        bug_file = BUG_DIR / f"bug_{task.id}.md"

        content = f"""
ID: BUG-{task.id}
Title: Failure in task {task.id}
Status: OPEN
Priority: HIGH

Source Task: {task.id}

Error:

{error}
"""

        bug_file.write_text(content.strip(), encoding="utf8")

        logger.error(f"BUG created for task {task.id}")

    # --------------------------------
    # run single task
    # --------------------------------

    def run_task(self, task: Task):

        try:

            task.set_status("RUNNING")

            result = self.execute_task(task)

            if result:

                task.set_status("DONE")

                logger.info(f"Task {task.id} DONE")

            else:

                raise RuntimeError("Task returned failure")

        except Exception:

            error = traceback.format_exc()

            logger.error(error)

            self.create_bug(task, error)

            task.set_status("FAILED")

    # --------------------------------
    # main loop
    # --------------------------------

    def run(self):

        logger.info("TaskExecutionEngine started")

        while True:

            state = self.autopilot_state()

            if state == "STOP":

                time.sleep(2)
                continue

            if state == "PAUSE":

                time.sleep(2)
                continue

            try:

                tasks = self.load_tasks()

                if not tasks:

                    time.sleep(5)
                    continue

                for task in tasks:

                    self.run_task(task)

            except Exception:

                logger.error(traceback.format_exc())

            time.sleep(2)


def main():

    engine = TaskExecutionEngine()

    engine.run()


if __name__ == "__main__":

    main()