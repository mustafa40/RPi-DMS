import cv2
from camera_manager import CameraManager
from face_detector import FaceDetector
from head_pose_detector import HeadPoseDetector

camera = CameraManager(camera_index=0, width=640, height=480, fps=15, flip=True)
face_detector = FaceDetector()
head_detector = HeadPoseDetector(frame_height=480, down_threshold=0.10, hold_time=0.8)

camera.open()

while True:
    ret, frame = camera.read()
    if not ret:
        break

    face = face_detector.detect(frame)

    if face is not None:
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    head_status, head_down = head_detector.update(face)

    color = (0, 255, 0)
    if head_down:
        color = (0, 0, 255)
    elif head_status == "HEAD CHECKING":
        color = (0, 165, 255)

    cv2.rectangle(frame, (0, 0), (640, 70), color, -1)
    cv2.putText(frame, head_status, (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow("Head Pose Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
