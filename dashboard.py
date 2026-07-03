import cv2


class Dashboard:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

    def draw(self, frame, status, alert_level, fps=0, blink_count=0):
        if alert_level in ["ALARM", "ALARM_1", "ALARM_2", "ALARM_3"]:
            theme = (0, 0, 255)
            status_text = "DROWSINESS ALERT"
        elif alert_level == "NO_FACE":
            theme = (0, 255, 255)
            status_text = "FACE NOT DETECTED"
        else:
            theme = (0, 180, 0)
            status_text = "NORMAL"

        cv2.rectangle(frame, (0, 0), (self.width, 75), theme, -1)

        cv2.putText(frame, "RPi-DMS v1.0", (15, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)

        cv2.putText(frame, status_text, (15, 62),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)

        cv2.rectangle(frame, (0, self.height - 95),
                      (self.width, self.height), (25, 25, 25), -1)

        cv2.putText(frame, f"STATUS : {status}", (15, self.height - 67),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

        cv2.putText(frame, f"ALERT  : {alert_level}", (15, self.height - 42),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, theme, 2)

        cv2.putText(frame, f"BLINK  : {blink_count}", (15, self.height - 17),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

        cv2.putText(frame, f"FPS: {fps:.1f}", (500, self.height - 17),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

        if alert_level in ["ALARM", "ALARM_1", "ALARM_2", "ALARM_3"]:
            cv2.rectangle(frame, (90, 150), (550, 305), (0, 0, 255), -1)
            cv2.putText(frame, "PLEASE TAKE", (180, 215),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
            cv2.putText(frame, "A BREAK", (230, 265),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)

        return frame
