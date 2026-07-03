import time


class FatigueEngine:
    def __init__(self, alarm_time=2.0):
        self.alarm_time = alarm_time
        self.closed_start = None
        self.status = "SYSTEM READY"
        self.alert_level = "NORMAL"

    def update(self, face_detected, eyes_open):
        now = time.time()

        if not face_detected:
            self.closed_start = None
            self.status = "NO FACE"
            self.alert_level = "NO_FACE"
            return self.status, self.alert_level

        if eyes_open:
            self.closed_start = None
            self.status = "EYES OPEN"
            self.alert_level = "NORMAL"
            return self.status, self.alert_level

        if self.closed_start is None:
            self.closed_start = now

        closed_time = now - self.closed_start

        if closed_time < self.alarm_time:
            self.status = f"EYES CLOSED: {closed_time:.1f}s"
            self.alert_level = "WARNING"
        else:
            self.status = "DROWSINESS ALERT"
            self.alert_level = "ALARM"

        return self.status, self.alert_level
