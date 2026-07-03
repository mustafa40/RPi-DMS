import cv2
import time


class YawningDetector:
    def __init__(self, yawn_time=1.0):
        self.mouth_cascade = cv2.CascadeClassifier(
            "/usr/share/opencv4/haarcascades/haarcascade_smile.xml"
        )
        self.yawn_time = yawn_time
        self.mouth_open_start = None
        self.yawning = False
        self.yawn_count = 0

    def detect(self, frame, face):
        x, y, w, h = face
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        lower_face = gray[y + int(h * 0.45):y + h, x:x + w]

        mouths = self.mouth_cascade.detectMultiScale(
            lower_face,
            scaleFactor=1.7,
            minNeighbors=18,
            minSize=(40, 25)
        )

        mouth_open = len(mouths) > 0

        now = time.time()

        if mouth_open:
            if self.mouth_open_start is None:
                self.mouth_open_start = now

            open_time = now - self.mouth_open_start

            if open_time >= self.yawn_time and not self.yawning:
                self.yawning = True
                self.yawn_count += 1

        else:
            self.mouth_open_start = None
            self.yawning = False

        detected_mouths = []
        for (mx, my, mw, mh) in mouths:
            detected_mouths.append((x + mx, y + int(h * 0.45) + my, mw, mh))

        return self.yawning, self.yawn_count, detected_mouths
