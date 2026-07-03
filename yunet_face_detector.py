import cv2


class YuNetFaceDetector:
    def __init__(self, model_path="models/face_detection_yunet_2023mar.onnx",
                 input_size=(640, 480), score_threshold=0.6):
        self.input_size = input_size
        self.detector = cv2.FaceDetectorYN.create(
            model_path,
            "",
            input_size,
            score_threshold,
            0.3,
            5000
        )

    def detect(self, frame):
        h, w = frame.shape[:2]

        if (w, h) != self.input_size:
            self.input_size = (w, h)
            self.detector.setInputSize(self.input_size)

        result, faces = self.detector.detect(frame)

        if faces is None:
            return None, False

        best = max(faces, key=lambda f: f[2] * f[3])

        x, y, bw, bh = best[:4].astype(int)

        x = max(0, x)
        y = max(0, y)

        return (x, y, bw, bh), True
