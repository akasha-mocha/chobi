import time
from threading import Lock


class TimedCache:

    def __init__(self, ttl=3):
        self.ttl = ttl
        self.data = None
        self.timestamp = 0
        self.lock = Lock()

    def get(self, loader):

        with self.lock:

            if self.data is None or time.time() - self.timestamp > self.ttl:

                self.data = loader()
                self.timestamp = time.time()

            return self.data