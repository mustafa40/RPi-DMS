import cv2
import time
from gpiozero import Buzzer

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

buzzer = Buzzer(18)

face_cascade = cv2.CascadeClassifier(
    "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    "/usr/share/opencv4/haarcascades/haarcascade_eye.xml"
)

closed_start = None
alarm_time = 2.0
alarm_active = False

last_face_time = time.time()
face_timeout = 1.0

eye_closed_frames = 0
eye_open_frames = 0

CLOSED_FRAME_LIMIT = 5
OPEN_FRAME_LIMIT = 3

while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.15,
        minNeighbors=4,
        minSize=(90, 90)
    )

    status = "YUZ ARANIYOR"
    color = (0, 255, 255)

    if len(faces) > 0:
        last_face_time = time.time()

        x, y, w, h = max(faces, key=lambda r: r[2] * r[3])

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        upper_face_gray = gray[y:y + int(h * 0.55), x:x+w]
        upper_face_color = frame[y:y + int(h * 0.55), x:x+w]

        eyes = eye_cascade.detectMultiScale(
            upper_face_gray,
            scaleFactor=1.12,
            minNeighbors=6,
            minSize=(22, 22),
            maxSize=(90, 70)
        )

        valid_eyes = []

        for (ex, ey, ew, eh) in eyes:
            if ey < h * 0.45 and ew > 20 and eh > 15:
                valid_eyes.append((ex, ey, ew, eh))
                cv2.rectangle(
                    upper_face_color,
                    (ex, ey),
                    (ex+ew, ey+eh),
                    (255, 0, 0),
                    2
                )

        if len(valid_eyes) >= 1:
            eye_open_frames += 1
            eye_closed_frames = 0

            if eye_open_frames >= OPEN_FRAME_LIMIT:
                status = "NORMAL - GOZ ACIK"
                color = (0, 255, 0)
                closed_start = None

                if alarm_active:
                    buzzer.off()
                    alarm_active = False

        else:
            eye_closed_frames += 1
            eye_open_frames = 0

            if eye_closed_frames >= CLOSED_FRAME_LIMIT:
                if closed_start is None:
                    closed_start = time.time()

                closed_time = time.time() - closed_start
                status = f"GOZ KAPALI: {closed_time:.1f} sn"
                color = (0, 0, 255)

                if closed_time >= alarm_time:
                    status = "UYARI! UYKU ALGILANDI"
                    color = (0, 0, 255)

                    if not alarm_active:
                        buzzer.on()
                        alarm_active = True
            else:
                status = "KONTROL EDILIYOR"
                color = (0, 165, 255)

    else:
        if time.time() - last_face_time > face_timeout:
            status = "YUZ YOK"
            color = (0, 255, 255)
            closed_start = None
            eye_closed_frames = 0
            eye_open_frames = 0

            if alarm_active:
                buzzer.off()
                alarm_active = False

    cv2.rectangle(frame, (0, 0), (640, 60), color, -1)
    cv2.putText(frame, status, (15, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)

    cv2.imshow("Driver Monitoring System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

buzzer.off()
cam.release()
cv2.destroyAllWindows()
