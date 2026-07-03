import time
from collections import deque


class PerclosTracker:
    def __init__(self, window_seconds=20):
        self.window_seconds = window_seconds
        self.samples = deque()

    def update(self, eyes_open):
        now = time.time()

        # eyes_closed: True/False
        eyes_closed = not eyes_open
        self.samples.append((now, eyes_closed))

        while self.samples and now - self.samples[0][0] > self.window_seconds:
            self.samples.popleft()

        if not self.samples:
            return 0.0

        closed_count = sum(1 for _, closed in self.samples if closed)
        total_count = len(self.samples)

        return (closed_count / total_count) * 100.0
