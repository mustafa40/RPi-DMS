import time


class FatigueEngine:
    def __init__(self, alarm_time=1.5, level2_time=3.5, level3_time=99.0):
        self.alarm_time = alarm_time
        self.level2_time = level2_time
        self.level3_time = level3_time
        self.closed_start = None

    def update(self, driver_state):
        now = time.time()

        if driver_state == "NO_FACE":
            self.closed_start = None
            return "NO FACE", "NO_FACE"

        if driver_state in ["ROAD", "DASHBOARD", "UNKNOWN"]:
            self.closed_start = None

            if driver_state == "DASHBOARD":
                return "LOOKING DASHBOARD", "NORMAL"

            if driver_state == "UNKNOWN":
                return "CHECKING EYES", "NORMAL"

            return "EYES OPEN", "NORMAL"

        if driver_state == "EYES_CLOSED":
            if self.closed_start is None:
                self.closed_start = now

            closed_time = now - self.closed_start

            if closed_time >= self.level3_time:
                return f"DROWSINESS ALERT L3: {closed_time:.1f}s", "ALARM_3"
            elif closed_time >= self.level2_time:
                return f"DROWSINESS ALERT L2: {closed_time:.1f}s", "ALARM_2"
            elif closed_time >= self.alarm_time:
                return f"DROWSINESS ALERT L1: {closed_time:.1f}s", "ALARM_1"
            else:
                return f"EYES CLOSED: {closed_time:.1f}s", "NORMAL"

        return "UNKNOWN", "NORMAL"
