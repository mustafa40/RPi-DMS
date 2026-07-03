import time
from gpiozero import Buzzer


class AlarmBuzzer:
    def __init__(self, gpio_pin=18):
        self.buzzer = Buzzer(gpio_pin)
        self.last_toggle = time.time()
        self.beep_state = False

    def off(self):
        self.buzzer.off()
        self.beep_state = False

    def update(self, alert_level):
        now = time.time()

        if alert_level == "ALARM_1":
            interval = 0.45
        elif alert_level == "ALARM_2":
            interval = 0.22
        elif alert_level == "ALARM_3":
            interval = 0.10
        else:
            self.off()
            return

        if now - self.last_toggle >= interval:
            self.last_toggle = now
            self.beep_state = not self.beep_state

            if self.beep_state:
                self.buzzer.on()
            else:
                self.buzzer.off()

    def cleanup(self):
        self.off()
