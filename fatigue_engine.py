import time


class FatigueEngine:
    def __init__(self, alarm_time=1.7, closed_confirm_frames=4, open_confirm_frames=3):
        self.alarm_time = alarm_time

        self.closed_confirm_frames = closed_confirm_frames
        self.open_confirm_frames = open_confirm_frames

        self.closed_frames = 0
        self.open_frames = 0

        self.confirmed_eyes_closed = False
        self.closed_start = None

        self.status = "SYSTEM READY"
        self.alert_level = "NORMAL"

    def update(self, face_detected, eyes_open):
        now = time.time()

        if not face_detected:
            self.closed_frames = 0
            self.open_frames = 0
            self.confirmed_eyes_closed = False
            self.closed_start = None
            self.status = "NO FACE"
            self.alert_level = "NO_FACE"
            return self.status, self.alert_level

        if eyes_open:
            self.open_frames += 1
            self.closed_frames = 0

            if self.open_frames >= self.open_confirm_frames:
                self.confirmed_eyes_closed = False
                self.closed_start = None
                self.status = "EYES OPEN"
                self.alert_level = "NORMAL"

            return self.status, self.alert_level

        else:
            self.closed_frames += 1
            self.open_frames = 0

            if self.closed_frames >= self.closed_confirm_frames:
                if not self.confirmed_eyes_closed:
                    self.confirmed_eyes_closed = True
                    self.closed_start = now

                closed_time = now - self.closed_start

                if closed_time < self.alarm_time:
                    self.status = f"EYES CLOSED: {closed_time:.1f}s"
                    self.alert_level = "WARNING"
                else:
                    self.status = "DROWSINESS ALERT"
                    self.alert_level = "ALARM"

            return self.status, self.alert_level
