from pathlib import Path
from scripts.utils.logger import get_logger
from scripts.ai.ai_runner import run_ai

logger = get_logger("goal_engine")

ROOT = Path(__file__).resolve().parents[2]

GOAL_FILE = ROOT / "knowledge/project_goal.md"
TASK_DIR = ROOT / "tickets/tasks"
BUG_DIR = ROOT / "tickets/bugs"


class GoalEngine:

    def load_goal(self):

        if not GOAL_FILE.exists():
            return ""

        with open(GOAL_FILE, encoding="utf8") as f:
            return f.read()

    def list_tasks(self):

        if not TASK_DIR.exists():
            return []

        return list(TASK_DIR.glob("*.md"))

    def list_bugs(self):

        if not BUG_DIR.exists():
            return []

        return list(BUG_DIR.glob("*.md"))

    def analyze_progress(self):

        goal = self.load_goal()

        tasks = self.list_tasks()
        bugs = self.list_bugs()

        task_list = "\n".join([t.name for t in tasks])
        bug_list = "\n".join([b.name for b in bugs])

        prompt = f"""
You are an autonomous software development AI.

Project Goal:

{goal}

Existing Tasks:

{task_list}

Existing Bugs:

{bug_list}

Analyze project progress.

Answer briefly:

1. Is the goal close to completion?
2. What should be the next development focus?
"""

        try:

            result = run_ai(prompt)

            logger.info("Goal analysis complete")

            return result

        except Exception as e:

            logger.error(str(e))
            return ""

    def log_progress(self, text):

        path = ROOT / "knowledge/goal_progress.md"

        with open(path, "a", encoding="utf8") as f:

            f.write("\n\n---\n\n")
            f.write(text)

    def run(self):

        goal = self.load_goal()

        if not goal:

            logger.warning("No project goal defined")
            return

        analysis = self.analyze_progress()

        if analysis:

            self.log_progress(analysis)