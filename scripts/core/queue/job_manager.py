import uuid

from scripts.core.queue.job_queue import JobQueue
from scripts.core.queue.job_worker import JobWorker
from scripts.core.queue.job_types import Job
from scripts.orchestrator.agent_coordinator import AgentCoordinator


class JobManager:

    def __init__(self, workers=3):

        self.queue = JobQueue()

        self.coordinator = AgentCoordinator()

        self.workers = []

        for _ in range(workers):

            w = JobWorker(self.queue, self.coordinator)

            w.start()

            self.workers.append(w)

    # ---------------------------------------------

    def submit_task(self, task):

        job = Job(

            id=str(uuid.uuid4()),
            type=task["type"],
            priority=self._priority(task),
            payload=task

        )

        self.queue.push(job)

        return job.id

    # ---------------------------------------------

    def _priority(self, task):

        if task["type"] == "bug":
            return 1

        if task["type"] == "test":
            return 2

        return 3

    # ---------------------------------------------

    def stop(self):

        for w in self.workers:
            w.stop()