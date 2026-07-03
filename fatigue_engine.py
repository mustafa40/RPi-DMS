import time


class FatigueEngine:
    def __init__(self, alarm_time=1.7, open_grace_time=0.35):
        self.alarm_time = alarm_time
        self.open_grace_time = open_grace_time

        self.closed_start = None
        self.last_closed_time = None

        self.status = "SYSTEM READY"
        self.alert_level = "NORMAL"

    def update(self, face_detected, eyes_open):
        now = time.time()

        if not face_detected:
            self.closed_start = None
            self.last_closed_time = None
            self.status = "NO FACE"
            self.alert_level = "NO_FACE"
            return self.status, self.alert_level

        if not eyes_open:
            if self.closed_start is None:
                self.closed_start = now

            self.last_closed_time = now
            closed_time = now - self.closed_start

            if closed_time >= self.alarm_time:
                self.status = "DROWSINESS ALERT"
                self.alert_level = "ALARM"
            else:
                self.status = f"EYES CLOSED: {closed_time:.1f}s"
                self.alert_level = "WARNING"

            return self.status, self.alert_level

        # eyes_open True olsa bile hemen sıfırlama.
        # Kısa süreli yanlış açık algılamayı tolere et.
        if self.closed_start is not None and self.last_closed_time is not None:
            open_gap = now - self.last_closed_time

            if open_gap < self.open_grace_time:
                closed_time = now - self.closed_start

                if closed_time >= self.alarm_time:
                    self.status = "DROWSINESS ALERT"
                    self.alert_level = "ALARM"
                else:
                    self.status = f"EYES CLOSED: {closed_time:.1f}s"
                    self.alert_level = "WARNING"

                return self.status, self.alert_level

        self.closed_start = None
        self.last_closed_time = None
        self.status = "EYES OPEN"
        self.alert_level = "NORMAL"
        return self.status, self.alert_level
