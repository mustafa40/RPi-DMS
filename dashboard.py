import cv2


class Dashboard:
    def draw(
        self,
        frame,
        status,
        alert_level,
        fps=0,
        blink_count=0,
        perclos=0,
        fatigue_score=0,
        driver_state="UNKNOWN",
        health_data=None
    ):
        h, w = frame.shape[:2]
        scale = max(0.65, h / 480.0)

        alarm_active = alert_level in [
            "ALARM",
            "ALARM_1",
            "ALARM_2",
            "ALARM_3"
        ]

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
        bottom_h = int(145 * scale)
        bottom_y = max(top_h, h - bottom_h)

        # -------------------------------------------------
        # ÜST DURUM ÇUBUĞU
        # -------------------------------------------------
        cv2.rectangle(frame, (0, 0), (w, top_h), theme, -1)

        cv2.putText(
            frame,
            "MFI DRIVER MONITORING",
            (int(14 * scale), int(27 * scale)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60 * scale,
            (0, 0, 0),
            max(1, int(2 * scale))
        )

        cv2.putText(
            frame,
            driver_status,
            (int(14 * scale), int(60 * scale)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.82 * scale,
            (0, 0, 0),
            max(1, int(2 * scale))
        )

        cv2.putText(
            frame,
            f"FPS {fps:.1f}",
            (w - int(110 * scale), int(28 * scale)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.46 * scale,
            (0, 0, 0),
            max(1, int(1 * scale))
        )

        # -------------------------------------------------
        # SÜRÜCÜ DURUMU KUTUSU
        # -------------------------------------------------
        state_x1 = int(10 * scale)
        state_y1 = top_h + int(8 * scale)
        state_x2 = min(w - 10, int(290 * scale))
        state_y2 = state_y1 + int(40 * scale)

        cv2.rectangle(
            frame,
            (state_x1, state_y1),
            (state_x2, state_y2),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            frame,
            f"DRIVER STATE: {driver_state}",
            (
                state_x1 + int(10 * scale),
                state_y1 + int(27 * scale)
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.53 * scale,
            (0, 255, 255),
            max(1, int(2 * scale))
        )

        # -------------------------------------------------
        # SÜRÜCÜ SAĞLIK PANELİ
        # -------------------------------------------------
        if health_data is None:
            health_data = {
                "heart_rate": None,
                "spo2": None,
                "status": "SENSOR OFFLINE",
                "source": "SENSOR"
            }

        health_w = int(235 * scale)
        health_h = int(120 * scale)

        health_x1 = max(
            int(w * 0.56),
            w - health_w - int(12 * scale)
        )

        health_y1 = top_h + int(8 * scale)
        health_x2 = w - int(10 * scale)
        health_y2 = min(
            bottom_y - int(8 * scale),
            health_y1 + health_h
        )

        if health_y2 > health_y1 + int(70 * scale):
            cv2.rectangle(
                frame,
                (health_x1, health_y1),
                (health_x2, health_y2),
                (18, 18, 18),
                -1
            )

            cv2.rectangle(
                frame,
                (health_x1, health_y1),
                (health_x2, health_y2),
                (0, 200, 200),
                max(1, int(2 * scale))
            )

            source = health_data.get("source", "SENSOR")
            heart_rate = health_data.get("heart_rate")
            spo2 = health_data.get("spo2")
            health_status = health_data.get(
                "status",
                "UNKNOWN"
            )

            hr_text = (
                "-- BPM"
                if heart_rate is None
                else f"{heart_rate} BPM"
            )

            spo2_text = (
                "-- %"
                if spo2 is None
                else f"{spo2} %"
            )

            cv2.putText(
                frame,
                f"DRIVER HEALTH - {source}",
                (
                    health_x1 + int(9 * scale),
                    health_y1 + int(22 * scale)
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.38 * scale,
                (0, 220, 220),
                max(1, int(1 * scale))
            )

            cv2.putText(
                frame,
                f"HEART RATE : {hr_text}",
                (
                    health_x1 + int(9 * scale),
                    health_y1 + int(49 * scale)
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45 * scale,
                (255, 255, 255),
                max(1, int(1 * scale))
            )

            cv2.putText(
                frame,
                f"SpO2       : {spo2_text}",
                (
                    health_x1 + int(9 * scale),
                    health_y1 + int(73 * scale)
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45 * scale,
                (255, 255, 255),
                max(1, int(1 * scale))
            )

            health_color = (
                (0, 220, 0)
                if health_status == "NORMAL"
                else (0, 140, 255)
            )

            cv2.putText(
                frame,
                f"STATUS     : {health_status}",
                (
                    health_x1 + int(9 * scale),
                    health_y1 + int(98 * scale)
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.40 * scale,
                health_color,
                max(1, int(1 * scale))
            )

        # -------------------------------------------------
        # ALT BİLGİ PANELİ
        # -------------------------------------------------
        cv2.rectangle(
            frame,
            (0, bottom_y),
            (w, h),
            (22, 22, 22),
            -1
        )

        left_x = int(14 * scale)
        middle_x = int(w * 0.50)

        cv2.putText(
            frame,
            f"STATUS  : {status}",
            (left_x, bottom_y + int(27 * scale)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48 * scale,
            (255, 255, 255),
            max(1, int(1 * scale))
        )

        cv2.putText(
            frame,
            f"ALERT   : {alert_level}",
            (left_x, bottom_y + int(53 * scale)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48 * scale,
            theme,
            max(1, int(2 * scale))
        )

        cv2.putText(
            frame,
            f"BLINK   : {blink_count}",
            (left_x, bottom_y + int(79 * scale)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48 * scale,
            (255, 255, 255),
            max(1, int(1 * scale))
        )

        cv2.putText(
            frame,
            f"PERCLOS : {perclos:.1f}%",
            (left_x, bottom_y + int(105 * scale)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48 * scale,
            (255, 255, 255),
            max(1, int(1 * scale))
        )

        cv2.putText(
            frame,
            f"FATIGUE SCORE : {fatigue_score}/100",
            (middle_x, bottom_y + int(35 * scale)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.49 * scale,
            theme,
            max(1, int(2 * scale))
        )

        # Yorgunluk göstergesi
        bar_x = middle_x
        bar_y = bottom_y + int(58 * scale)
        bar_w = max(80, int(w * 0.40))
        bar_h = max(10, int(18 * scale))

        cv2.rectangle(
            frame,
            (bar_x, bar_y),
            (
                min(w - 10, bar_x + bar_w),
                bar_y + bar_h
            ),
            (80, 80, 80),
            1
        )

        fill_w = int(
            bar_w
            * min(max(fatigue_score, 0), 100)
            / 100
        )

        cv2.rectangle(
            frame,
            (bar_x, bar_y),
            (
                min(w - 10, bar_x + fill_w),
                bar_y + bar_h
            ),
            theme,
            -1
        )

        cv2.putText(
            frame,
            "Health data: UI simulation",
            (middle_x, bottom_y + int(108 * scale)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.32 * scale,
            (150, 150, 150),
            max(1, int(1 * scale))
        )

        # -------------------------------------------------
        # ALARM EKRANI
        # -------------------------------------------------
        if alarm_active:
            x1 = int(w * 0.12)
            y1 = int(h * 0.30)
            x2 = int(w * 0.88)
            y2 = int(h * 0.61)

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 180),
                -1
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 255, 255),
                max(2, int(3 * scale))
            )

            cv2.putText(
                frame,
                "DROWSINESS DETECTED",
                (
                    x1 + int(30 * scale),
                    y1 + int(65 * scale)
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.95 * scale,
                (255, 255, 255),
                max(2, int(3 * scale))
            )

            cv2.putText(
                frame,
                "PLEASE TAKE A BREAK",
                (
                    x1 + int(45 * scale),
                    y1 + int(120 * scale)
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.78 * scale,
                (255, 255, 255),
                max(2, int(3 * scale))
            )

        return frame
