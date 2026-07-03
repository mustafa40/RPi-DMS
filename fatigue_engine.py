import time


class FatigueEngine:
    def __init__(
        self,
        alarm_time=1.7,
        level2_time=3.7,
        level3_time=99.0,
        open_confirm_time=0.7
    ):
        self.alarm_time = alarm_time
        self.level2_time = level2_time
        self.level3_time = level3_time
        self.open_confirm_time = open_confirm_time

        self.closed_start = None
        self.open_start = None

    def update(self, face_detected, eyes_open):
        now = time.time()

        if not face_detected:
            self.closed_start = None
            self.open_start = None
            return "NO FACE", "NO_FACE"

        if not eyes_open:
            self.open_start = None

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

        # Göz açık algılandı ama hemen normale dönme.
        # 0.7 sn boyunca açık kalırsa gerçekten açıldı kabul et.
        if self.open_start is None:
            self.open_start = now

        open_time = now - self.open_start

        if self.closed_start is not None and open_time < self.open_confirm_time:
            closed_time = now - self.closed_start

            if closed_time >= self.level2_time:
                return f"DROWSINESS ALERT L2: {closed_time:.1f}s", "ALARM_2"
            elif closed_time >= self.alarm_time:
                return f"DROWSINESS ALERT L1: {closed_time:.1f}s", "ALARM_1"
            else:
                return f"EYES CLOSED: {closed_time:.1f}s", "NORMAL"

        self.closed_start = None
        self.open_start = None
        return "EYES OPEN", "NORMAL"
