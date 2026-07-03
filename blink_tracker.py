class BlinkTracker:
    def __init__(self):
        self.blink_count = 0
        self.was_closed = False

    def update(self, eyes_open):
        if not eyes_open and not self.was_closed:
            self.was_closed = True

        if eyes_open and self.was_closed:
            self.blink_count += 1
            self.was_closed = False

        return self.blink_count

    def reset(self):
        self.blink_count = 0
        self.was_closed = False
