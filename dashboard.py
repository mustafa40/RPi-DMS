import cv2


class Dashboard:
    def draw(self, frame, status, alert_level, fps=0, blink_count=0,
             perclos=0, fatigue_score=0, driver_state="UNKNOWN"):

        h, w = frame.shape[:2]
        scale = h / 480.0

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

        top_h = int(72 * scale)
        panel_h = int(128 * scale)
        panel_y = h - panel_h

        # Top bar
        cv2.rectangle(frame, (0, 0), (w, top_h), theme, -1)

        cv2.putText(frame, "MFI DMS",
                    (int(15 * scale), int(28 * scale)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75 * scale, (0, 0, 0),
                    max(1, int(2 * scale)))

        cv2.putText(frame, driver_status,
                    (int(15 * scale), int(61 * scale)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9 * scale, (0, 0, 0),
                    max(1, int(2 * scale)))

        cv2.putText(frame, f"FPS {fps:.1f}",
                    (w - int(130 * scale), int(30 * scale)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55 * scale, (0, 0, 0),
                    max(1, int(2 * scale)))

        # State black box
        cv2.rectangle(frame,
                      (int(10 * scale), int(82 * scale)),
                      (int(285 * scale), int(120 * scale)),
                      (0, 0, 0), -1)

        cv2.putText(frame, f"STATE: {driver_state}",
                    (int(20 * scale), int(110 * scale)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65 * scale, (0, 255, 255),
                    max(1, int(2 * scale)))

        # Bottom panel
        cv2.rectangle(frame, (0, panel_y), (w, h), (22, 22, 22), -1)

        left_x = int(15 * scale)
        right_x = int(w * 0.52)

        cv2.putText(frame, f"STATUS  : {status}",
                    (left_x, panel_y + int(26 * scale)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.50 * scale, (255, 255, 255),
                    max(1, int(2 * scale)))

        cv2.putText(frame, f"ALERT   : {alert_level}",
                    (left_x, panel_y + int(51 * scale)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.50 * scale, theme,
                    max(1, int(2 * scale)))

        cv2.putText(frame, f"BLINK   : {blink_count}",
                    (left_x, panel_y + int(76 * scale)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.50 * scale, (255, 255, 255),
                    max(1, int(2 * scale)))

        cv2.putText(frame, f"PERCLOS : {perclos:.1f}%",
                    (left_x, panel_y + int(101 * scale)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.50 * scale, (255, 255, 255),
                    max(1, int(2 * scale)))

        cv2.putText(frame, f"FATIGUE : {fatigue_score}/100",
                    (right_x, panel_y + int(51 * scale)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.58 * scale, theme,
                    max(1, int(2 * scale)))

        # Fatigue bar
        bar_x = right_x
        bar_y = panel_y + int(75 * scale)
        bar_w = int(w * 0.38)
        bar_h = int(18 * scale)

        cv2.rectangle(frame, (bar_x, bar_y),
                      (bar_x + bar_w, bar_y + bar_h),
                      (80, 80, 80), 1)

        fill_w = int(bar_w * min(max(fatigue_score, 0), 100) / 100)
        cv2.rectangle(frame, (bar_x, bar_y),
                      (bar_x + fill_w, bar_y + bar_h),
                      theme, -1)

        # Alarm overlay
        if alarm_active:
            x1, y1 = int(w * 0.12), int(h * 0.30)
            x2, y2 = int(w * 0.88), int(h * 0.62)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 180), -1)
            cv2.rectangle(frame, (x1, y1), (x2, y2),
                          (255, 255, 255), max(2, int(3 * scale)))

            cv2.putText(frame, "DROWSINESS",
                        (x1 + int(75 * scale), y1 + int(70 * scale)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.1 * scale, (255, 255, 255),
                        max(2, int(3 * scale)))

            cv2.putText(frame, "PLEASE TAKE A BREAK",
                        (x1 + int(35 * scale), y1 + int(130 * scale)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.82 * scale, (255, 255, 255),
                        max(2, int(3 * scale)))

        return frame
