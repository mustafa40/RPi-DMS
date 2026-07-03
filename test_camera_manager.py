import cv2
from camera_manager import CameraManager

camera = CameraManager(camera_index=0, width=640, height=480, fps=15, flip=True)
camera.open()

while True:
    ret, frame = camera.read()

    if not ret:
        print("Goruntu alinamadi")
        break

    fps = camera.get_fps()

    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow("Camera Manager Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
