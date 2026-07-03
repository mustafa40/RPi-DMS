import time


class FatigueEngine:
    def __init__(self, alarm_time=1.7, level2_time=3.0, level3_time=5.0, open_grace_time=0.35):
        self.alarm_time = alarm_time
        self.level2_time = level2_time
        self.level3_time = level3_time
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

            if closed_time >= self.level3_time:
                self.status = f"DROWSINESS ALERT L3: {closed_time:.1f}s"
                self.alert_level = "ALARM_3"
            elif closed_time >= self.level2_time:
                self.status = f"DROWSINESS ALERT L2: {closed_time:.1f}s"
                self.alert_level = "ALARM_2"
            elif closed_time >= self.alarm_time:
                self.status = f"DROWSINESS ALERT L1: {closed_time:.1f}s"
                self.alert_level = "ALARM_1"
            else:
                self.status = f"EYES CLOSED: {closed_time:.1f}s"
                self.alert_level = "NORMAL"

            return self.status, self.alert_level

        if self.closed_start is not None and self.last_closed_time is not None:
            open_gap = now - self.last_closed_time

            if open_gap < self.open_grace_time:
                closed_time = now - self.closed_start

                if closed_time >= self.level3_time:
                    self.status = f"DROWSINESS ALERT L3: {closed_time:.1f}s"
                    self.alert_level = "ALARM_3"
                elif closed_time >= self.level2_time:
                    self.status = f"DROWSINESS ALERT L2: {closed_time:.1f}s"
                    self.alert_level = "ALARM_2"
                elif closed_time >= self.alarm_time:
                    self.status = f"DROWSINESS ALERT L1: {closed_time:.1f}s"
                    self.alert_level = "ALARM_1"
                else:
                    self.status = f"EYES CLOSED: {closed_time:.1f}s"
                    self.alert_level = "NORMAL"

                return self.status, self.alert_level

        self.closed_start = None
        self.last_closed_time = None
        self.status = "EYES OPEN"
        self.alert_level = "NORMAL"
        return self.status, self.alert_level
