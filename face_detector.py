import cv2
import time


class FaceDetector:
    def __init__(self, memory_time=1.7):
        self.front_cascade = cv2.CascadeClassifier(
            "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
        )
        self.profile_cascade = cv2.CascadeClassifier(
            "/usr/share/opencv4/haarcascades/haarcascade_profileface.xml"
        )

        self.last_face = None
        self.last_seen_time = 0
        self.memory_time = memory_time

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = []

        front_faces = self.front_cascade.detectMultiScale(
            gray, scaleFactor=1.12, minNeighbors=3, minSize=(70, 70)
        )
        faces.extend(front_faces)

        profile_faces = self.profile_cascade.detectMultiScale(
            gray, scaleFactor=1.12, minNeighbors=3, minSize=(70, 70)
        )
        faces.extend(profile_faces)

        flipped_gray = cv2.flip(gray, 1)
        profile_faces_flipped = self.profile_cascade.detectMultiScale(
            flipped_gray, scaleFactor=1.12, minNeighbors=3, minSize=(70, 70)
        )

        for (x, y, w, h) in profile_faces_flipped:
            x_original = frame.shape[1] - x - w
            faces.append((x_original, y, w, h))

        if len(faces) > 0:
            self.last_face = max(faces, key=lambda r: r[2] * r[3])
            self.last_seen_time = time.time()
            return self.last_face, True

        if self.last_face is not None and time.time() - self.last_seen_time < self.memory_time:
            return self.last_face, False

        return None, False
