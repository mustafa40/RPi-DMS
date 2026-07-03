import time
from gpiozero import Buzzer


class AlarmBuzzer:
    def __init__(self, gpio_pin=18):
        self.buzzer = Buzzer(gpio_pin)
        self.last_change = time.time()
        self.beep_on = False
        self.last_level = "NORMAL"

    def off(self):
        self.buzzer.off()
        self.beep_on = False

    def update(self, alert_level):
        now = time.time()

        if alert_level != self.last_level:
            self.last_level = alert_level
            self.last_change = now
            self.beep_on = False
            self.buzzer.off()

        if alert_level == "ALARM_1":
            on_time = 0.12
            off_time = 0.80

        elif alert_level == "ALARM_2":
            on_time = 0.12
            off_time = 0.25

        elif alert_level == "ALARM_3":
            self.buzzer.on()
            return

        else:
            self.off()
            return

        if self.beep_on:
            if now - self.last_change >= on_time:
                self.buzzer.off()
                self.beep_on = False
                self.last_change = now
        else:
            if now - self.last_change >= off_time:
                self.buzzer.on()
                self.beep_on = True
                self.last_change = now

    def cleanup(self):
        self.off()
