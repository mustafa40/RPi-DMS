import cv2
from camera_manager import CameraManager
from face_detector import FaceDetector
from yawning_detector import YawningDetector

camera = CameraManager(camera_index=0, width=640, height=480, fps=15, flip=True)
face_detector = FaceDetector(memory_time=1.2)
yawn_detector = YawningDetector(yawn_time=1.0)

camera.open()

while True:
    ret, frame = camera.read()
    if not ret:
        break

    face, real_face = face_detector.detect(frame)

    status = "NO FACE"
    yawn_count = 0

    if face is not None:
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        yawning, yawn_count, mouths = yawn_detector.detect(frame, face)

        for (mx, my, mw, mh) in mouths:
            cv2.rectangle(frame, (mx, my), (mx+mw, my+mh), (0, 0, 255), 2)

        status = "YAWNING" if yawning else "NORMAL"

    cv2.putText(frame, f"YAWN: {status}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    cv2.putText(frame, f"COUNT: {yawn_count}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    cv2.imshow("Yawning Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
