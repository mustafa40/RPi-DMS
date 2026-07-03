import cv2
from camera_manager import CameraManager
from face_detector import FaceDetector
from eye_detector import EyeDetector

camera = CameraManager(camera_index=0, width=640, height=480, fps=15, flip=True)
face_detector = FaceDetector()
eye_detector = EyeDetector()

camera.open()

while True:
    ret, frame = camera.read()
    if not ret:
        break

    face = face_detector.detect(frame)

    if face is not None:
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        eyes = eye_detector.detect(frame, face)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

        status = "EYES OPEN" if eye_detector.is_open(eyes) else "EYES CLOSED"
    else:
        status = "NO FACE"

    cv2.putText(frame, status, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Eye Detector Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
