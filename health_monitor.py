import glob
import time
from typing import Any, Dict, Optional

import serial


class HealthMonitor:
    def __init__(
        self,
        baudrate: int = 115200,
        data_timeout: float = 5.0
    ) -> None:
        self.baudrate = baudrate
        self.data_timeout = data_timeout

        self.serial_port: Optional[
            serial.Serial
        ] = None

        self.port_name: Optional[str] = None

        self.heart_rate: Optional[int] = None
        self.spo2: Optional[int] = None
        self.finger_detected = False

        self.last_message_time = 0.0
        self.last_connection_attempt = 0.0

        self._connect()

    def _find_nucleo_port(self) -> Optional[str]:
        ports = sorted(
            glob.glob("/dev/ttyACM*")
            + glob.glob("/dev/ttyUSB*")
        )

        return ports[0] if ports else None

    def _connect(self) -> bool:
        if self.serial_port is not None:
            return True

        now = time.time()

        if now - self.last_connection_attempt < 2.0:
            return False

        self.last_connection_attempt = now

        port = self._find_nucleo_port()

        if port is None:
            self.port_name = None
            return False

        try:
            self.serial_port = serial.Serial(
                port=port,
                baudrate=self.baudrate,
                timeout=0.01
            )

            self.port_name = port

            time.sleep(1.5)
            self.serial_port.reset_input_buffer()

            return True

        except (serial.SerialException, OSError):
            self.serial_port = None
            self.port_name = None
            return False

    def _disconnect(self) -> None:
        if self.serial_port is not None:
            try:
                self.serial_port.close()
            except (serial.SerialException, OSError):
                pass

        self.serial_port = None
        self.port_name = None

    def _clear_measurements(self) -> None:
        self.heart_rate = None
        self.spo2 = None

    def _parse_line(self, line: str) -> bool:
        line = line.strip()

        if not line.startswith("HEALTH,"):
            return False

        parts = line.split(",")

        if len(parts) != 4:
            return False

        try:
            bpm = int(float(parts[1]))
            spo2_value = int(float(parts[2]))
            finger_value = int(parts[3])

        except (ValueError, TypeError):
            return False

        self.last_message_time = time.time()
        self.finger_detected = finger_value == 1

        if not self.finger_detected:
            self._clear_measurements()
            return True

        self.heart_rate = (
            bpm
            if 35 <= bpm <= 220
            else None
        )

        self.spo2 = (
            spo2_value
            if 70 <= spo2_value <= 100
            else None
        )

        return True

    def _read_latest_message(self) -> None:
        if self.serial_port is None:
            return

        latest_health_line: Optional[str] = None

        try:
            while self.serial_port.in_waiting > 0:
                raw_line = self.serial_port.readline()

                line = raw_line.decode(
                    "utf-8",
                    errors="ignore"
                ).strip()

                if line.startswith("HEALTH,"):
                    latest_health_line = line

            if latest_health_line is not None:
                self._parse_line(latest_health_line)

        except (serial.SerialException, OSError):
            self._disconnect()

    def _calculate_status(self) -> str:
        if not self.finger_detected:
            return "PLACE FINGER"

        if (
            self.heart_rate is None
            or self.spo2 is None
        ):
            return "MEASURING"

        if self.spo2 < 94:
            return "LOW SpO2"

        if self.heart_rate < 50:
            return "LOW HEART RATE"

        if self.heart_rate > 120:
            return "HIGH HEART RATE"

        return "NORMAL"

    def update(self) -> Dict[str, Any]:
        if self.serial_port is None:
            self._connect()

        if self.serial_port is None:
            return {
                "heart_rate": None,
                "spo2": None,
                "status": "SENSOR OFFLINE",
                "finger_detected": False,
                "finger_status": "NOT DETECTED",
                "source": "NUCLEO"
            }

        self._read_latest_message()

        now = time.time()

        if (
            self.last_message_time == 0.0
            or now - self.last_message_time
            > self.data_timeout
        ):
            self.finger_detected = False
            self._clear_measurements()

            return {
                "heart_rate": None,
                "spo2": None,
                "status": "NO DATA",
                "finger_detected": False,
                "finger_status": "NOT DETECTED",
                "source": "NUCLEO"
            }

        return {
            "heart_rate": self.heart_rate,
            "spo2": self.spo2,
            "status": self._calculate_status(),
            "finger_detected":
                self.finger_detected,
            "finger_status": (
                "DETECTED"
                if self.finger_detected
                else "NOT DETECTED"
            ),
            "source": "LIVE SENSOR"
        }

    def close(self) -> None:
        self._disconnect()
