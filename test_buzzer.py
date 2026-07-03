from time import sleep
from alarm_buzzer import AlarmBuzzer

alarm = AlarmBuzzer(gpio_pin=18)

print("Buzzer test basladi")
alarm.on()
sleep(1)
alarm.off()
print("Buzzer test bitti")
