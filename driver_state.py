import time


class DriverStateAnalyzer:
    ROAD = "ROAD"
    DASHBOARD = "DASHBOARD"
    EYES_CLOSED = "EYES_CLOSED"
    NO_FACE = "NO_FACE"
    UNKNOWN = "UNKNOWN"

    def __init__(self, frame_height=480):
        self.frame_height = frame_height
        self.last_eyes_open_time = time.time()
        self.last_face_center_y = None

    def update(self, face_detected, face, eyes_open):
        now = time.time()

        if not face_detected or face is None:
            return self.NO_FACE

        x, y, w, h = face
        face_center_y = (y + h / 2) / self.frame_height

        if eyes_open:
            self.last_eyes_open_time = now
            self.last_face_center_y = face_center_y
            return self.ROAD

        eyes_missing_time = now - self.last_eyes_open_time

        if self.last_face_center_y is not None:
            y_shift = face_center_y - self.last_face_center_y
        else:
            y_shift = 0

        # Çok kısa göz kaybı: kırpma / anlık hata
        if eyes_missing_time < 0.4:
            return self.UNKNOWN

        # Kısa süreli aşağı bakış: gösterge paneli
        if y_shift > 0.06 and eyes_missing_time < 1.5:
            return self.DASHBOARD

        # 1.5 saniyeden uzun göz görünmüyorsa artık uyku riski kabul et
        return self.EYES_CLOSED
