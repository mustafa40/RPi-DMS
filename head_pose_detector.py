import time


class HeadPoseDetector:
    def __init__(self, frame_height=480, down_threshold=0.10, hold_time=0.8):
        self.frame_height = frame_height
        self.down_threshold = down_threshold
        self.hold_time = hold_time

        self.baseline_y = None
        self.down_start = None

    def update(self, face):
        if face is None:
            self.down_start = None
            return "NO_FACE", False

        x, y, w, h = face

        face_center_y = (y + h / 2) / self.frame_height

        if self.baseline_y is None:
            self.baseline_y = face_center_y

        # Baş normal konumdayken baseline yavaş yavaş güncellensin
        if face_center_y < self.baseline_y + self.down_threshold:
            self.baseline_y = (self.baseline_y * 0.98) + (face_center_y * 0.02)
            self.down_start = None
            return "HEAD NORMAL", False

        # Baş aşağı düştüyse süre tut
        if self.down_start is None:
            self.down_start = time.time()

        down_time = time.time() - self.down_start

        if down_time >= self.hold_time:
            return "HEAD DOWN", True

        return "HEAD CHECKING", False
