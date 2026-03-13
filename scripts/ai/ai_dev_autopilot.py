import time
from pathlib import Path

from scripts.utils.logger import get_logger
from scripts.ai.task_execution_engine import TaskExecutionEngine
from scripts.ai.task_generator import TaskGenerator
from scripts.ai.goal_engine import GoalEngine

logger = get_logger("ai_autopilot")

ROOT = Path(__file__).resolve().parents[2]

TASK_DIR = ROOT / "tickets/tasks"
BUG_DIR = ROOT / "tickets/bugs"
STATE_FILE = ROOT / "runtime/autopilot_state.txt"


class AutopilotState:
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


def read_state():

    if not STATE_FILE.exists():
        return AutopilotState.RUNNING

    try:

        with open(STATE_FILE, encoding="utf8") as f:
            state = f.read().strip()

        if state == "":
            return AutopilotState.RUNNING

        return state

    except Exception:
        return AutopilotState.RUNNING


def write_state(state):

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(STATE_FILE, "w", encoding="utf8") as f:
        f.write(state)


class AIDevAutopilot:

    def __init__(self):

        self.goal_engine = GoalEngine()
        self.task_generator = TaskGenerator()
        self.task_engine = TaskExecutionEngine()

        # safety limits
        self.max_tasks = 5
        self.max_bugs = 10
        self.loop_interval = 5

    # -----------------------------
    # helpers
    # -----------------------------

    def count_tasks(self):

        if not TASK_DIR.exists():
            return 0

        return len(list(TASK_DIR.glob("*.md")))

    def count_bugs(self):

        if not BUG_DIR.exists():
            return 0

        return len(list(BUG_DIR.glob("*.md")))

    # -----------------------------
    # main loop
    # -----------------------------

    def loop(self):

        logger.info("AI Dev Autopilot started")

        write_state(AutopilotState.RUNNING)

        while True:

            state = read_state()

            if state == AutopilotState.STOPPED:

                logger.info("Autopilot stopped")
                break

            if state == AutopilotState.PAUSED:

                logger.info("Autopilot paused")
                time.sleep(self.loop_interval)
                continue

            try:

                # -----------------------------
                # Goal analysis
                # -----------------------------

                self.goal_engine.run()

                # -----------------------------
                # Task generation
                # -----------------------------

                task_count = self.count_tasks()

                if task_count < self.max_tasks:

                    logger.info("Generating new task")

                    self.task_generator.run()

                else:

                    logger.info("Task queue full")

                # -----------------------------
                # Task execution
                # -----------------------------

                self.task_engine.run_next_task()

                # -----------------------------
                # Bug monitoring
                # -----------------------------

                bug_count = self.count_bugs()

                if bug_count > self.max_bugs:

                    logger.warning(
                        f"Bug count exceeded limit ({bug_count})"
                    )

                # -----------------------------
                # loop sleep
                # -----------------------------

                time.sleep(self.loop_interval)

            except Exception as e:

                logger.error(str(e))

                time.sleep(self.loop_interval)


# -------------------------------------
# entry point
# -------------------------------------

def run_autopilot():

    autopilot = AIDevAutopilot()

    autopilot.loop()