from scripts.agents.planning.planner_agent import PlannerAgent
from scripts.agents.development.coder_agent import CoderAgent
from scripts.agents.testing.test_agent import TestAgent
from scripts.agents.bugfix.bugfix_agent import BugfixAgent
from scripts.agents.architecture.architect_agent import ArchitectAgent

from scripts.utils.logger import get_logger

logger = get_logger(__name__)


class AgentCoordinator:

    def __init__(self):

        self.agents = {
            "plan": PlannerAgent(),
            "code": CoderAgent(),
            "test": TestAgent(),
            "bugfix": BugfixAgent(),
            "architecture": ArchitectAgent(),
        }

    def select_agent(self, task):

        t = task["type"]

        if t == "feature":
            return self.agents["code"]

        if t == "test":
            return self.agents["test"]

        if t == "bug":
            return self.agents["bugfix"]

        if t == "architecture":
            return self.agents["architecture"]

        if t == "plan":
            return self.agents["plan"]

        return self.agents["code"]

    def run(self, task):

        agent = self.select_agent(task)

        logger.info(f"Agent selected: {agent.__class__.__name__}")

        return agent.run(task)