import cv2
from camera_manager import CameraManager
from face_detector import FaceDetector

camera = CameraManager(camera_index=0, width=640, height=480, fps=15, flip=True)
face_detector = FaceDetector()

camera.open()

while True:
    ret, frame = camera.read()
    if not ret:
        break

    face = face_detector.detect(frame)

    if face is not None:
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "FACE", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "NO FACE", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Face Detector Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
