import time
from max30102_driver import MAX30102


sensor = MAX30102()
sensor.setup()

print("MAX30102 RAW TEST")
print("Part ID:", hex(sensor.part_id()))
print("Parmak yokken ve parmak varken degerleri izle.")
print()

while True:
    red, ir = sensor.read_latest()

    if red is not None:
        finger = "FINGER" if ir > 1000 else "NO FINGER"
        print(f"RED: {red:8d} | IR: {ir:8d} | {finger}")

    time.sleep(0.05)
