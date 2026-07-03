import time


class FatigueEngine:
    def __init__(self, alarm_time=1.7, level2_time=3.0, level3_time=5.0, open_grace_time=0.35):
        self.alarm_time = alarm_time
        self.level2_time = level2_time
        self.level3_time = level3_time
        self.open_grace_time = open_grace_time
        self.closed_start = None
        self.last_closed_time = None

    def update(self, face_detected, eyes_open):
        now = time.time()

        if not face_detected:
            self.closed_start = None
            self.last_closed_time = None
            return "NO FACE", "NO_FACE"

        if not eyes_open:
            if self.closed_start is None:
                self.closed_start = now

            self.last_closed_time = now
            closed_time = now - self.closed_start

            if closed_time >= self.level3_time:
                return f"DROWSINESS ALERT L3: {closed_time:.1f}s", "ALARM_3"
            elif closed_time >= self.level2_time:
                return f"DROWSINESS ALERT L2: {closed_time:.1f}s", "ALARM_2"
            elif closed_time >= self.alarm_time:
                return f"DROWSINESS ALERT L1: {closed_time:.1f}s", "ALARM_1"
            else:
                return f"EYES CLOSED: {closed_time:.1f}s", "NORMAL"

        if self.closed_start is not None and self.last_closed_time is not None:
            if now - self.last_closed_time < self.open_grace_time:
                closed_time = now - self.closed_start

                if closed_time >= self.level3_time:
                    return f"DROWSINESS ALERT L3: {closed_time:.1f}s", "ALARM_3"
                elif closed_time >= self.level2_time:
                    return f"DROWSINESS ALERT L2: {closed_time:.1f}s", "ALARM_2"
                elif closed_time >= self.alarm_time:
                    return f"DROWSINESS ALERT L1: {closed_time:.1f}s", "ALARM_1"
                else:
                    return f"EYES CLOSED: {closed_time:.1f}s", "NORMAL"

        self.closed_start = None
        self.last_closed_time = None
        return "EYES OPEN", "NORMAL"
