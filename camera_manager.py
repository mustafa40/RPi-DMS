import cv2
import time


class CameraManager:
    def __init__(self, camera_index=0, width=640, height=480, fps=15, flip=True):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps
        self.flip = flip
        self.cap = None
        self.last_time = time.time()
        self.current_fps = 0

    def open(self):
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_V4L2)

        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            raise RuntimeError("Kamera acilamadi")

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return False, None

        if self.flip:
            frame = cv2.flip(frame, 1)

        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        if dt > 0:
            self.current_fps = 1.0 / dt

        return True, frame

    def get_fps(self):
        return self.current_fps

    def release(self):
        if self.cap is not None:
            self.cap.release()
