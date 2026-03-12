class TaskDependencyGraph:

    def __init__(self):
        self.graph = {}

    def add_task(self, task_id):

        if task_id not in self.graph:
            self.graph[task_id] = []

    def add_dependency(self, task, depends_on):

        self.add_task(task)
        self.add_task(depends_on)

        self.graph[task].append(depends_on)

    def get_dependencies(self, task_id):

        return self.graph.get(task_id, [])