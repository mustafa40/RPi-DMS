import cv2


class EyeDetector:
    def __init__(self):
        self.eye_cascade = cv2.CascadeClassifier(
            "/usr/share/opencv4/haarcascades/haarcascade_eye.xml"
        )

    def detect(self, frame, face):
        x, y, w, h = face

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        upper_gray = gray[y:y + int(h * 0.55), x:x + w]

        eyes = self.eye_cascade.detectMultiScale(
            upper_gray,
            scaleFactor=1.12,
            minNeighbors=6,
            minSize=(22, 22),
            maxSize=(90, 70)
        )

        valid_eyes = []

        for (ex, ey, ew, eh) in eyes:
            if ey < h * 0.45 and ew > 20 and eh > 15:
                valid_eyes.append((x + ex, y + ey, ew, eh))

        return valid_eyes

    def is_open(self, eyes):
        return len(eyes) >= 1
