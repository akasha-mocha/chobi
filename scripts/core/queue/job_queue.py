import queue


class JobQueue:

    def __init__(self):

        self.q = queue.PriorityQueue()

    def push(self, job):

        self.q.put((job.priority, job))

    def pop(self):

        if self.q.empty():
            return None

        return self.q.get()[1]

    def size(self):

        return self.q.qsize()