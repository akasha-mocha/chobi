import time

from scripts.tasks.task_manager import TaskManager
from scripts.testing.test_runner import run_tests
from scripts.bugs.bug_manager import BugManager


class JobWorker:

    def __init__(self):

        self.tasks = TaskManager()
        self.bugs = BugManager()

    def execute_task(self, task):

        print(f"[Worker] executing {task['title']}")

        # ここにAI生成などを入れる
        success = True

        if not success:
            self.bugs.create_bug(task)
            return

        test_ok = run_tests()

        if test_ok:

            self.tasks.complete(task["id"])
            print("[Worker] task complete")

        else:

            self.bugs.create_bug(task)
            print("[Worker] test failed -> bug created")

    def run(self):

        print("[Worker] started")

        while True:

            task = self.tasks.get_next_task()

            if task:
                self.execute_task(task)

            time.sleep(3)