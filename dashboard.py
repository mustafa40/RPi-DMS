import cv2


class Dashboard:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

    def draw(self, frame, status, alert_level, fps=0, blink_count=0):
        if alert_level == "ALARM":
            color = (0, 0, 255)
        elif alert_level == "WARNING":
            color = (0, 165, 255)
        elif alert_level == "NO_FACE":
            color = (0, 255, 255)
        else:
            color = (0, 255, 0)

        cv2.rectangle(frame, (0, 0), (self.width, 90), color, -1)

        cv2.putText(frame, "RPi-DMS v1.0", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

        cv2.putText(frame, status, (15, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

        cv2.rectangle(frame, (0, self.height - 70),
                      (self.width, self.height), (30, 30, 30), -1)

        cv2.putText(frame, f"ALERT: {alert_level}", (15, self.height - 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

        cv2.putText(frame, f"BLINK: {blink_count}", (15, self.height - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

        cv2.putText(frame, f"FPS: {fps:.1f}", (500, self.height - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

        return frame
