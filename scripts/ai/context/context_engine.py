from scripts.ai.ai_context_engine import build_context
from scripts.utils.logger import get_logger

logger = get_logger(__name__)


class Worker:

    def __init__(self, coordinator):

        self.coordinator = coordinator

    def prepare_context(self, task):

        context = build_context(task)

        return context

    def execute(self, task):

        try:

            logger.info(f"Worker executing task {task['id']}")

            context = self.prepare_context(task)

            task["context"] = context

            result = self.coordinator.run(task)

            return {
                "status": "done",
                "result": result
            }

        except Exception as e:

            logger.error(f"Worker failure: {e}")

            return {
                "status": "failed",
                "error": str(e)
            }