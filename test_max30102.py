import time
from max30102_reader import MAX30102Reader
 
 
sensor = MAX30102Reader()
sensor.setup()
 
print("MAX30102 basladi. Parmagini sensorun ustune koy.")
 
while True:
    red, ir = sensor.read_fifo()
    print(f"RED: {red:6d} | IR: {ir:6d}")
    time.sleep(0.1)
