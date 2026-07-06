import time
from max30102_reader import MAX30102Reader


sensor = MAX30102Reader()
sensor.setup()

print("MAX30102 test basladi.")
print("Part ID:", hex(sensor.part_id()))
print("Parmagini sensorun uzerine hafif bastir.")
print("IR 10000 ustune cikarsa parmak algilaniyor demektir.")
print()

while True:
    red, ir = sensor.read_latest()

    if red is None:
        print("FIFO bos...")
    else:
        finger = "FINGER" if ir > 10000 else "NO FINGER"
        print(f"RED: {red:7d} | IR: {ir:7d} | {finger}")

    time.sleep(0.1)
