"""
Chobi AI Dev Autopilot

AIが自動で

Goal
 ↓
Task生成
 ↓
Task計画
 ↓
Task実行
 ↓
Bug修正

を繰り返す
"""

import time

from scripts.ai.goal_engine import GoalEngine
from scripts.ai.task_generator import TaskGenerator
from scripts.ai.task_execution_engine import TaskExecutionEngine
from scripts.ai.bug_auto_fix_engine import BugAutoFixEngine
from scripts.planning.task_manager import TaskManager
from scripts.planning.task_planner import TaskPlanner
from scripts.utils.logger import get_logger


logger = get_logger("AI_AUTOPILOT")


class AIDevAutopilot:

    def __init__(self):

        self.goal_engine = GoalEngine()
        self.task_generator = TaskGenerator()
        self.task_planner = TaskPlanner()
        self.task_manager = TaskManager()
        self.executor = TaskExecutionEngine()
        self.bug_fixer = BugAutoFixEngine()

        self.running = True

    def run(self):

        logger.info("AI Dev Autopilot Started")

        while self.running:

            try:

                self.dev_cycle()

            except Exception as e:

                logger.error(f"Autopilot error: {e}")

            time.sleep(3)

    def dev_cycle(self):

        logger.info("----- Dev Cycle Start -----")

        goal = self.get_goal()

        if not goal:
            logger.info("No goal found")
            return

        logger.info(f"Goal: {goal}")

        tasks = self.generate_tasks(goal)

        if not tasks:
            logger.info("No tasks generated")
            return

        tasks = self.plan_tasks(tasks)

        self.save_tasks(tasks)

        self.execute_tasks()

        self.fix_bugs()

        logger.info("----- Dev Cycle End -----")

    def get_goal(self):

        goal = self.goal_engine.get_current_goal()

        return goal

    def generate_tasks(self, goal):

        logger.info("Generating tasks")

        tasks = self.task_generator.generate(goal)

        logger.info(f"{len(tasks)} tasks generated")

        return tasks

    def plan_tasks(self, tasks):

        logger.info("Planning tasks")

        tasks = self.task_planner.plan(tasks)

        return tasks

    def save_tasks(self, tasks):

        logger.info("Saving tasks")

        for task in tasks:

            self.task_manager.create_task(task)

    def execute_tasks(self):

        logger.info("Executing tasks")

        tasks = self.task_manager.get_pending_tasks()

        for task in tasks:

            logger.info(f"Executing task {task['id']}")

            result = self.executor.execute(task)

            if result["success"]:

                self.task_manager.complete_task(task["id"])

            else:

                self.task_manager.fail_task(
                    task["id"],
                    result["error"]
                )

    def fix_bugs(self):

        logger.info("Bug fixing")

        bugs = self.task_manager.get_failed_tasks()

        for bug in bugs:

            fix = self.bug_fixer.fix(bug)

            if fix["success"]:

                self.task_manager.complete_task(bug["id"])

            else:

                logger.warning(f"Bug fix failed {bug['id']}")

    def stop(self):

        self.running = False


def run_autopilot():

    autopilot = AIDevAutopilot()

    autopilot.run()


if __name__ == "__main__":

    run_autopilot()