import cv2

from camera_manager import CameraManager
from face_detector import FaceDetector
from eye_detector import EyeDetector
from fatigue_engine import FatigueEngine
from alarm_buzzer import AlarmBuzzer
from dashboard import Dashboard
from blink_tracker import BlinkTracker


camera = CameraManager(camera_index=0, width=640, height=480, fps=15, flip=True)
face_detector = FaceDetector(memory_time=1.2)
eye_detector = EyeDetector()
engine = FatigueEngine(alarm_time=1.7)
alarm = AlarmBuzzer(gpio_pin=18)
dashboard = Dashboard(width=640, height=480)
blink_tracker = BlinkTracker()

camera.open()

try:
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        face, real_face = face_detector.detect(frame)

        face_detected = face is not None
        eyes_open = False

        if face_detected:
            x, y, w, h = face

            face_color = (0, 255, 0) if real_face else (0, 165, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), face_color, 2)

            eyes = eye_detector.detect(frame, face)
            eyes_open = eye_detector.is_open(eyes)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

        blink_count = blink_tracker.update(eyes_open)

        status, alert_level = engine.update(face_detected, eyes_open)

        if alert_level == "ALARM":
            alarm.on()
        else:
            alarm.off()

        frame = dashboard.draw(
            frame=frame,
            status=status,
            alert_level=alert_level,
            fps=camera.get_fps(),
            blink_count=blink_count
        )

        cv2.imshow("RPi-DMS Professional", frame)
        

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    alarm.cleanup()
    camera.release()
    cv2.destroyAllWindows()
