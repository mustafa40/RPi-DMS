import cv2

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


camera = CameraManager(camera_index=0, width=640, height=480, fps=15, flip=True)
face_detector = FaceDetector(memory_time=1.2)
eye_detector = EyeDetector()
driver_state_analyzer = DriverStateAnalyzer(frame_height=480)
engine = FatigueEngine(alarm_time=0.6, level2_time=2.5, level3_time=99.0)
alarm = AlarmBuzzer(gpio_pin=18)
dashboard = Dashboard(width=640, height=480)
blink_tracker = BlinkTracker()
perclos_tracker = PerclosTracker(window_seconds=20)
fatigue_score_engine = FatigueScore()

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
        detect_this_frame = frame_count % 3 == 0

        if detect_this_frame:
            face, real_face = face_detector.detect(frame)
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
            face_color = (0, 255, 0) if real_face else (0, 165, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), face_color, 2)

            if detect_this_frame:
                eyes = eye_detector.detect(frame, face)
                eyes_open = eye_detector.is_open(eyes)
                last_eyes = eyes
                last_eyes_open = eyes_open

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)
        else:
            last_eyes = []
            last_eyes_open = False
            eyes_open = False

        driver_state = driver_state_analyzer.update(
            face_detected=face_detected,
            face=face,
            eyes_open=eyes_open
        )

        blink_count = blink_tracker.update(eyes_open)
        perclos = perclos_tracker.update(eyes_open)
        fatigue_score = fatigue_score_engine.update(driver_state, perclos)

        status, alert_level = engine.update(driver_state)

        alarm.update(alert_level)

        cv2.putText(frame, f"STATE: {driver_state}", (20, 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        frame = dashboard.draw(
            frame=frame,
            status=status,
            alert_level=alert_level,
            fps=camera.get_fps(),
            blink_count=blink_count,
            perclos=perclos,
            fatigue_score=fatigue_score
        )

        cv2.imshow("RPi-DMS Professional", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    alarm.cleanup()
    camera.release()
    cv2.destroyAllWindows()
