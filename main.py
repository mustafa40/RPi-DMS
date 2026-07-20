import cv2
import config

from camera_manager import CameraManager
from face_detector import FaceDetector
from eye_detector import EyeDetector
from driver_state import DriverStateAnalyzer
from fatigue_engine import FatigueEngine
from alarm_buzzer import AlarmBuzzer
from dashboard import Dashboard
from blink_tracker import BlinkTracker
from perclos_tracker import PerclosTracker
from fatigue_score import FatigueScore
from splash_screen import show_splash
from health_monitor import HealthMonitor


def get_screen_size():
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()

        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()

        root.destroy()

        return width, height

    except Exception:
        return 800, 480


def main():
    screen_w, screen_h = get_screen_size()
    window_name = config.WINDOW_NAME

    # Tam ekran OpenCV penceresi
    cv2.namedWindow(
        window_name,
        cv2.WND_PROP_FULLSCREEN
    )

    cv2.setWindowProperty(
        window_name,
        cv2.WND_PROP_FULLSCREEN,
        cv2.WINDOW_FULLSCREEN
    )

    # MFI açılış ekranı
    show_splash(
        window_name,
        screen_w,
        screen_h
    )

    camera = CameraManager(
        camera_index=0,
        width=config.CAMERA_WIDTH,
        height=config.CAMERA_HEIGHT,
        fps=config.CAMERA_FPS,
        flip=config.CAMERA_FLIP
    )

    face_detector = FaceDetector(
        memory_time=1.2
    )

    eye_detector = EyeDetector()

    driver_state_analyzer = DriverStateAnalyzer(
        frame_height=config.DRIVER_STATE_FRAME_HEIGHT
    )

    engine = FatigueEngine(
        alarm_time=config.ALARM_TIME,
        level2_time=config.ALARM_LEVEL2_TIME,
        level3_time=config.ALARM_LEVEL3_TIME
    )

    alarm = AlarmBuzzer(
        gpio_pin=config.BUZZER_GPIO
    )

    dashboard = Dashboard()

    blink_tracker = BlinkTracker()

    perclos_tracker = PerclosTracker(
        window_seconds=config.PERCLOS_WINDOW_SECONDS
    )

    fatigue_score_engine = FatigueScore()

    # MAX30102 hazır olana kadar simülasyon modu
    health_monitor = HealthMonitor(
        simulation=True
    )

    camera.open()

    frame_count = 0

    last_face = None
    last_real_face = False
    last_eyes = []
    last_eyes_open = False

    try:
        while True:
            ret, frame = camera.read()

            if not ret:
                break

            frame_count += 1

            # Performans için üç karede bir algılama
            detect_this_frame = (
                frame_count % 3 == 0
            )

            if detect_this_frame:
                face, real_face = (
                    face_detector.detect(frame)
                )

                last_face = face
                last_real_face = real_face

            else:
                face = last_face
                real_face = last_real_face

            face_detected = face is not None

            eyes_open = last_eyes_open
            eyes = last_eyes

            if face_detected:
                x, y, w, h = face

                face_color = (
                    (0, 255, 0)
                    if real_face
                    else (0, 165, 255)
                )

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    face_color,
                    2
                )

                if detect_this_frame:
                    eyes = eye_detector.detect(
                        frame,
                        face
                    )

                    eyes_open = (
                        eye_detector.is_open(eyes)
                    )

                    last_eyes = eyes
                    last_eyes_open = eyes_open

                for ex, ey, ew, eh in eyes:
                    cv2.rectangle(
                        frame,
                        (ex, ey),
                        (ex + ew, ey + eh),
                        (255, 0, 0),
                        2
                    )

            else:
                last_eyes = []
                last_eyes_open = False
                eyes_open = False

            driver_state = (
                driver_state_analyzer.update(
                    face_detected=face_detected,
                    face=face,
                    eyes_open=eyes_open
                )
            )

            blink_count = (
                blink_tracker.update(eyes_open)
            )

            perclos = (
                perclos_tracker.update(eyes_open)
            )

            fatigue_score = (
                fatigue_score_engine.update(
                    driver_state,
                    perclos
                )
            )

            status, alert_level = (
                engine.update(driver_state)
            )

            # Buzzer alarm seviyesi
            alarm.update(alert_level)

            # Sağlık verileri
            health_data = (
                health_monitor.update()
            )

            # Dashboard
            frame = dashboard.draw(
                frame=frame,
                status=status,
                alert_level=alert_level,
                fps=camera.get_fps(),
                blink_count=blink_count,
                perclos=perclos,
                fatigue_score=fatigue_score,
                driver_state=driver_state,
                health_data=health_data
            )

            # Takılı ekranın tamamına sığdır
            display = cv2.resize(
                frame,
                (screen_w, screen_h),
                interpolation=cv2.INTER_LINEAR
            )

            cv2.imshow(
                window_name,
                display
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == 27:
                break

    finally:
        alarm.cleanup()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
