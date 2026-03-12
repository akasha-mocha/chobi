import json
from pathlib import Path

from scripts.tasks.task_manager import TaskManager
from scripts.utils.logger import get_logger
from scripts.ai.ai_interface import AIInterface


class SelfPlanner:

    """
    AI Self Planning System

    spec → tasks を自動生成
    """

    def __init__(self):

        self.logger = get_logger("self_planner")

        self.task_manager = TaskManager()

        self.ai = AIInterface()

    def load_spec(self):

        spec_file = Path("docs/spec.yaml")

        if not spec_file.exists():

            raise Exception("spec.yaml not found")

        return spec_file.read_text()

    def load_prompt(self):

        prompt_file = Path(
            ".antigravity/prompts/generation/break_tasks.md"
        )

        return prompt_file.read_text()

    def build_prompt(self, spec):

        template = self.load_prompt()

        prompt = template.replace("{{SPEC}}", spec)

        return prompt

    def generate_tasks(self):

        self.logger.info("Generating tasks from spec")

        spec = self.load_spec()

        prompt = self.build_prompt(spec)

        response = self.ai.run(prompt)

        tasks = self.parse_tasks(response)

        self.logger.info(f"{len(tasks)} tasks generated")

        for task in tasks:

            self.task_manager.create_task(task)

        return tasks

    def parse_tasks(self, response):

        """
        AI response → tasks
        """

        try:

            data = json.loads(response)

            return data["tasks"]

        except Exception:

            self.logger.error("AI task parsing failed")

            return []

    def run(self):

        self.logger.info("SelfPlanner started")

        tasks = self.generate_tasks()

        return tasks