import cv2
import time


class FaceDetector:
    def __init__(self, memory_time=0.8):
        self.face_cascade = cv2.CascadeClassifier(
            "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
        )
        self.last_face = None
        self.last_seen_time = 0
        self.memory_time = memory_time

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.12,
            minNeighbors=3,
            minSize=(70, 70)
        )

        if len(faces) > 0:
            self.last_face = max(faces, key=lambda r: r[2] * r[3])
            self.last_seen_time = time.time()
            return self.last_face, True

        if self.last_face is not None:
            if time.time() - self.last_seen_time < self.memory_time:
                return self.last_face, False

        return None, False
