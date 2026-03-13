import time
import traceback
from pathlib import Path
from typing import List, Dict

from scripts.utils.logger import get_logger

logger = get_logger("ai_autopilot")

ROOT = Path(__file__).resolve().parents[2]

TASK_DIR = ROOT / "tickets/tasks"
BUG_DIR = ROOT / "tickets/bugs"
KNOWLEDGE_DIR = ROOT / "knowledge"
STATE_FILE = ROOT / "runtime/autopilot_state.txt"


# -----------------------------------------
# state
# -----------------------------------------

class AutopilotState:

    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


def set_state(state: str):

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(STATE_FILE, "w", encoding="utf8") as f:
        f.write(state)


def get_state():

    if not STATE_FILE.exists():
        return AutopilotState.STOPPED

    with open(STATE_FILE, encoding="utf8") as f:
        return f.read().strip()


# -----------------------------------------
# file utils
# -----------------------------------------

def read_md(path: Path) -> str:

    with open(path, encoding="utf8") as f:
        return f.read()


def write_md(path: Path, text: str):

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf8") as f:
        f.write(text)


# -----------------------------------------
# task manager
# -----------------------------------------

def list_tasks() -> List[Path]:

    if not TASK_DIR.exists():
        return []

    return list(TASK_DIR.glob("*.md"))


def list_bugs() -> List[Path]:

    if not BUG_DIR.exists():
        return []

    return list(BUG_DIR.glob("*.md"))


def next_task():

    tasks = list_tasks()

    if not tasks:
        return None

    return tasks[0]


# -----------------------------------------
# planner
# -----------------------------------------

class Planner:

    def plan(self):

        logger.info("Planning tasks...")

        tasks = list_tasks()

        if tasks:
            return

        task = """ID: TASK-1
Title: Improve dashboard UI
Status: OPEN
Priority: MEDIUM
"""

        write_md(TASK_DIR / "task_001.md", task)

        logger.info("Task created")


# -----------------------------------------
# code generator
# -----------------------------------------

class CodeGenerator:

    def run(self, task_path: Path):

        logger.info(f"Generating code for {task_path}")

        # placeholder for LLM

        time.sleep(1)

        return True


# -----------------------------------------
# tester
# -----------------------------------------

class Tester:

    def run(self):

        logger.info("Running tests")

        time.sleep(1)

        return True


# -----------------------------------------
# bug detector
# -----------------------------------------

class BugDetector:

    def run(self) -> List[Dict]:

        logger.info("Scanning for bugs")

        # placeholder

        return []


# -----------------------------------------
# bug fixer
# -----------------------------------------

class BugFixer:

    def fix(self, bug):

        logger.info(f"Fixing bug {bug}")

        time.sleep(1)


# -----------------------------------------
# knowledge manager
# -----------------------------------------

class KnowledgeManager:

    def update(self, text: str):

        path = KNOWLEDGE_DIR / "autopilot_log.md"

        old = ""

        if path.exists():
            old = read_md(path)

        write_md(path, old + "\n" + text)


# -----------------------------------------
# main loop
# -----------------------------------------

class AIDevAutopilot:

    def __init__(self):

        self.planner = Planner()
        self.codegen = CodeGenerator()
        self.tester = Tester()
        self.detector = BugDetector()
        self.fixer = BugFixer()
        self.knowledge = KnowledgeManager()

    # -----------------------------

    def run_task(self, task_path: Path):

        logger.info(f"Running task {task_path}")

        ok = self.codegen.run(task_path)

        if not ok:
            logger.error("Code generation failed")
            return

        test_ok = self.tester.run()

        if not test_ok:

            bug = {
                "title": "Test failed",
                "task": task_path.name
            }

            self.create_bug(bug)

    # -----------------------------

    def create_bug(self, bug):

        bug_id = int(time.time())

        path = BUG_DIR / f"bug_{bug_id}.md"

        text = f"""
ID: BUG-{bug_id}
Title: {bug['title']}
Status: OPEN
Priority: HIGH
Task: {bug['task']}
"""

        write_md(path, text)

        logger.warning(f"Bug created {path}")

    # -----------------------------

    def handle_bugs(self):

        bugs = list_bugs()

        for bug_path in bugs:

            logger.info(f"Handling bug {bug_path}")

            bug_text = read_md(bug_path)

            bug = {
                "title": bug_text
            }

            self.fixer.fix(bug)

    # -----------------------------

    def loop(self):

        logger.info("AI Dev Autopilot started")

        set_state(AutopilotState.RUNNING)

        while True:

            state = get_state()

            if state == AutopilotState.STOPPED:
                logger.info("Autopilot stopped")
                break

            if state == AutopilotState.PAUSED:
                time.sleep(2)
                continue

            try:

                self.planner.plan()

                task = next_task()

                if task:
                    self.run_task(task)

                self.handle_bugs()

                self.knowledge.update("loop executed")

            except Exception:

                logger.error(traceback.format_exc())

            time.sleep(5)


# -----------------------------------------
# entry
# -----------------------------------------

def run_autopilot():

    autopilot = AIDevAutopilot()

    autopilot.loop()