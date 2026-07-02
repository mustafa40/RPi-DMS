import cv2

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cam.isOpened():
    print("Kamera acilamadi")
    exit()

while True:
    ret, frame = cam.read()
    if not ret:
        print("Goruntu alinamadi")
        break

    cv2.imshow("Logitech Kamera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
