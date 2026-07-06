import cv2
import os
import numpy as np
import config


def show_splash(window_name, screen_w, screen_h):
    splash_path = os.path.join(os.path.dirname(__file__), config.SPLASH_IMAGE)
    img = cv2.imread(splash_path)

    if img is None:
        img = np.ones((screen_h, screen_w, 3), dtype=np.uint8) * 255
        cv2.putText(img, "MARTUR FOMPAK INTERNATIONAL",
                    (40, screen_h // 2 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (80, 80, 80), 2)
        cv2.putText(img, "Connectivity & Smart Devices",
                    (80, screen_h // 2 + 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 100, 100), 2)
    else:
        img = cv2.resize(img, (screen_w, screen_h))

    cv2.imshow(window_name, img)
    cv2.waitKey(config.SPLASH_TIME_MS)
