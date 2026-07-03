from gpiozero import Buzzer


class AlarmBuzzer:
    def __init__(self, gpio_pin=18):
        self.buzzer = Buzzer(gpio_pin)
        self.active = False

    def on(self):
        if not self.active:
            self.buzzer.on()
            self.active = True

    def off(self):
        if self.active:
            self.buzzer.off()
            self.active = False

    def cleanup(self):
        self.buzzer.off()
        self.active = False
