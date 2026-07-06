import time
from max30102_reader import MAX30102Reader


sensor = MAX30102Reader()
sensor.setup()

print("MAX30102 basladi")
print("Part ID:", hex(sensor.part_id()))
print("Parmagini sensorun ustune koy")
print()

while True:
    red, ir = sensor.read_latest()

    if red is None:
        print("FIFO BOS")
    else:
        finger = "FINGER" if ir > 5000 else "NO FINGER"
        print(f"RED: {red:8d} | IR: {ir:8d} | {finger}")

    time.sleep(0.1)
