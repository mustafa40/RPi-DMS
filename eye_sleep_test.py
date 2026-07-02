import cv2
import time

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

face_cascade = cv2.CascadeClassifier(
    "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    "/usr/share/opencv4/haarcascades/haarcascade_eye.xml"
)

closed_start = None
alarm_time = 2.0

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(80, 80))

    status = "YUZ YOK"
    color = (0, 255, 255)

    for (x, y, w, h) in faces:
        face_gray = gray[y:y+h, x:x+w]
        face_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(face_gray, 1.2, 5, minSize=(20, 20))

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

        if len(eyes) >= 1:
            status = "NORMAL - GOZ ACIK"
            color = (0, 255, 0)
            closed_start = None
        else:
            if closed_start is None:
                closed_start = time.time()

            closed_time = time.time() - closed_start
            status = f"GOZ KAPALI: {closed_time:.1f} sn"
            color = (0, 0, 255)

            if closed_time >= alarm_time:
                status = "UYARI! UYKU ALGILANDI"

        break

    cv2.rectangle(frame, (0, 0), (640, 60), color, -1)
    cv2.putText(frame, status, (15, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

    cv2.imshow("Eye Sleep Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
