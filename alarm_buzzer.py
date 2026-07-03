import time
from gpiozero import Buzzer


class AlarmBuzzer:
    def __init__(self, gpio_pin=18):
        self.buzzer = Buzzer(gpio_pin)
        self.active = False
        self.last_toggle = time.time()
        self.beep_state = False

    def on(self):
        self.buzzer.on()
        self.active = True

    def off(self):
        self.buzzer.off()
        self.active = False
        self.beep_state = False

    def update(self, alert_level):
        now = time.time()

        if alert_level == "ALARM":
            # Gerçek DMS gibi: bip bip bip
            if now - self.last_toggle >= 0.25:
                self.last_toggle = now
                self.beep_state = not self.beep_state

                if self.beep_state:
                    self.buzzer.on()
                else:
                    self.buzzer.off()

        elif alert_level == "WARNING":
            # Uyarı seviyesinde kısa aralıklı hafif bip
            if now - self.last_toggle >= 0.8:
                self.last_toggle = now
                self.beep_state = not self.beep_state

                if self.beep_state:
                    self.buzzer.on()
                else:
                    self.buzzer.off()
        else:
            self.off()

    def cleanup(self):
        self.off()
