import math
import time


class HealthMonitor:
    """
    MAX30102 hazır olana kadar açıkça belirtilen simülasyon verileri üretir.

    Gerçek sensör çalıştırıldığında yalnızca bu sınıf değiştirilecek.
    Dashboard ve main.py aynı kalabilir.
    """

    def __init__(self, simulation=True):
        self.simulation = simulation
        self.start_time = time.time()

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
        heart_rate = int(
            74
            + 3 * math.sin(elapsed / 3.0)
            + math.sin(elapsed / 0.9)
        )

        spo2 = int(
            98
            + 0.7 * math.sin(elapsed / 5.0)
        )

        heart_rate = max(68, min(heart_rate, 82))
        spo2 = max(96, min(spo2, 99))

        if heart_rate < 50 or heart_rate > 120:
            health_status = "HR WARNING"
        elif spo2 < 94:
            health_status = "LOW OXYGEN"
        else:
            health_status = "NORMAL"

        return {
            "heart_rate": heart_rate,
            "spo2": spo2,
            "status": health_status,
            "finger_detected": True,
            "source": "SIMULATED"
        }
