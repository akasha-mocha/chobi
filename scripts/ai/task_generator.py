from pathlib import Path
import time
from scripts.utils.logger import get_logger
from scripts.ai.ai_runner import run_ai

logger = get_logger("task_generator")

ROOT = Path(__file__).resolve().parents[2]

TASK_DIR = ROOT / "tickets/tasks"
BUG_DIR = ROOT / "tickets/bugs"
KNOWLEDGE_DIR = ROOT / "knowledge"


class TaskGenerator:

    def list_tasks(self):

        if not TASK_DIR.exists():
            return []

        return list(TASK_DIR.glob("*.md"))

    def list_bugs(self):

        if not BUG_DIR.exists():
            return []

        return list(BUG_DIR.glob("*.md"))

    def load_knowledge(self):

        text = ""

        if not KNOWLEDGE_DIR.exists():
            return text

        for f in KNOWLEDGE_DIR.glob("*.md"):

            try:
                with open(f, encoding="utf8") as fp:
                    text += fp.read() + "\n"
            except:
                pass

        return text

    def generate_task(self):

        tasks = self.list_tasks()
        bugs = self.list_bugs()
        knowledge = self.load_knowledge()

        task_summary = "\n".join([t.name for t in tasks])
        bug_summary = "\n".join([b.name for b in bugs])

        prompt = f"""
You are an autonomous software development AI.

Project knowledge:
{knowledge}

Existing tasks:
{task_summary}

Existing bugs:
{bug_summary}

Generate ONE new development task.

Format:

ID: TASK-XXXX
Title: short title
Status: OPEN
Priority: MEDIUM

Description:
Explain the task.
"""

        return run_ai(prompt)

    def save_task(self, text):

        task_id = int(time.time())

        path = TASK_DIR / f"task_{task_id}.md"

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf8") as f:
            f.write(text)

        logger.info(f"Task created {path}")

    def run(self):

        tasks = self.list_tasks()

        if len(tasks) >= 5:
            return

        try:

            task = self.generate_task()

            if task:
                self.save_task(task)

        except Exception as e:

            logger.error(str(e))