import cv2


class Dashboard:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

    def draw(self, frame, status, alert_level, fps=0, blink_count=0, perclos=0, fatigue_score=0):
        alarm_active = alert_level in ["ALARM", "ALARM_1", "ALARM_2", "ALARM_3"]

        if alarm_active:
            theme = (0, 0, 255)
            driver_status = "TAKE A BREAK"
        elif alert_level == "NO_FACE":
            theme = (0, 220, 220)
            driver_status = "FACE LOST"
        elif fatigue_score >= 60:
            theme = (0, 140, 255)
            driver_status = "FATIGUE RISK"
        else:
            theme = (0, 180, 0)
            driver_status = "ATTENTIVE"

        # Top bar
        cv2.rectangle(frame, (0, 0), (self.width, 78), theme, -1)
        cv2.putText(frame, "RPi-DMS LITE", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
        cv2.putText(frame, driver_status, (15, 64),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

        cv2.putText(frame, f"FPS {fps:.1f}", (515, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)

        # Bottom info panel
        panel_y = self.height - 135
        cv2.rectangle(frame, (0, panel_y), (self.width, self.height), (22, 22, 22), -1)

        cv2.putText(frame, f"STATUS  : {status}", (15, panel_y + 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 2)

        cv2.putText(frame, f"ALERT   : {alert_level}", (15, panel_y + 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, theme, 2)

        cv2.putText(frame, f"BLINK   : {blink_count}", (15, panel_y + 82),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 2)

        cv2.putText(frame, f"PERCLOS : {perclos:.1f}%", (15, panel_y + 109),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 2)

        cv2.putText(frame, f"FATIGUE : {fatigue_score}/100", (330, panel_y + 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.58, theme, 2)

        # Fatigue bar
        bar_x, bar_y = 330, panel_y + 78
        bar_w, bar_h = 260, 18
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (80, 80, 80), 1)

        fill_w = int(bar_w * min(max(fatigue_score, 0), 100) / 100)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h), theme, -1)

        # Alarm overlay
        if alarm_active:
            cv2.rectangle(frame, (70, 130), (570, 305), (0, 0, 180), -1)
            cv2.rectangle(frame, (70, 130), (570, 305), (255, 255, 255), 3)

            cv2.putText(frame, "DROWSINESS", (160, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 3)

            cv2.putText(frame, "PLEASE TAKE A BREAK", (105, 260),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 255, 255), 3)

        return frame
