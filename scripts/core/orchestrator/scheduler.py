from scripts.tasks.task_priority_engine import TaskPriorityEngine
from scripts.tasks.task_dependency_graph import TaskDependencyGraph
from scripts.utils.logger import get_logger

logger = get_logger(__name__)


class Scheduler:

    def __init__(self, task_manager):

        self.task_manager = task_manager

        self.priority_engine = TaskPriorityEngine()

        self.dep_graph = TaskDependencyGraph()

    def _filter_ready_tasks(self, tasks):

        ready = []

        for t in tasks:

            if self.dep_graph.is_ready(t):
                ready.append(t)

        return ready

    def next_task(self):

        tasks = self.task_manager.get_pending_tasks()

        if not tasks:
            return None

        ready_tasks = self._filter_ready_tasks(tasks)

        if not ready_tasks:
            logger.info("Waiting for dependencies")
            return None

        prioritized = self.priority_engine.sort(ready_tasks)

        return prioritized[0]