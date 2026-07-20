import math
import time


class HealthMonitor:
    """
    Demo sağlık verisi üretir.

    MAX30102 çalışınca bu sınıfın update() fonksiyonu
    gerçek sensör değerlerini döndürecek şekilde değiştirilecek.
    """

    def __init__(self, simulation=True):
        self.simulation = simulation
        self.start_time = time.time()

        self.heart_rate = None
        self.spo2 = None
        self.status = "SENSOR OFFLINE"
        self.finger_detected = False

    def update(self):
        if not self.simulation:
            return {
                "heart_rate": None,
                "spo2": None,
                "status": "SENSOR OFFLINE",
                "finger_detected": False,
                "source": "SENSOR"
            }

        elapsed = time.time() - self.start_time

        # Videoda doğal görünmesi için yavaş değişen demo değerleri
        self.heart_rate = int(
            74
            + 3 * math.sin(elapsed / 3.0)
            + 1 * math.sin(elapsed / 0.9)
        )

        self.spo2 = int(
            98
            + 0.7 * math.sin(elapsed / 5.0)
        )

        self.heart_rate = max(68, min(self.heart_rate, 82))
        self.spo2 = max(96, min(self.spo2, 99))

        self.finger_detected = True

        if self.heart_rate < 50 or self.heart_rate > 120:
            self.status = "HEART RATE WARNING"
        elif self.spo2 < 94:
            self.status = "LOW OXYGEN"
        else:
            self.status = "NORMAL"

        return {
            "heart_rate": self.heart_rate,
            "spo2": self.spo2,
            "status": self.status,
            "finger_detected": self.finger_detected,
            "source": "SIMULATED"
        }
