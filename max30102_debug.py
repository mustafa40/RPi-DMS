import time
import smbus

ADDR = 0x57
bus = smbus.SMBus(1)

def w(reg, val):
    bus.write_byte_data(ADDR, reg, val)

def r(reg):
    return bus.read_byte_data(ADDR, reg)

def setup():
    w(0x09, 0x40)
    time.sleep(0.5)

    # interrupt clear
    r(0x00)
    r(0x01)

    # FIFO reset
    w(0x04, 0x00)
    w(0x05, 0x00)
    w(0x06, 0x00)

    # FIFO avg=1, rollover on
    w(0x08, 0x0F)

    # SPO2 config: ADC range 16384nA, 100Hz, 411us
    w(0x0A, 0x67)

    # LED currents
    w(0x0C, 0xFF)  # RED
    w(0x0D, 0xFF)  # IR

    # Multi LED slot config
    # slot1 = RED, slot2 = IR
    w(0x11, 0x21)
    w(0x12, 0x00)

    # Multi LED mode
    w(0x09, 0x07)

    time.sleep(0.5)

def read_fifo():
    data = bus.read_i2c_block_data(ADDR, 0x07, 6)
    led1 = ((data[0] << 16) | (data[1] << 8) | data[2]) & 0x3FFFF
    led2 = ((data[3] << 16) | (data[4] << 8) | data[5]) & 0x3FFFF
    return led1, led2

setup()

print("PART ID:", hex(r(0xFF)))
print("MODE:", hex(r(0x09)))
print("SPO2:", hex(r(0x0A)))
print("FIFO:", hex(r(0x08)))
print("LED1:", hex(r(0x0C)))
print("LED2:", hex(r(0x0D)))
print("Basladi. Parmak yok / parmak var farkina bak.")
print()

while True:
    wr = r(0x04)
    rd = r(0x06)
    avail = (wr - rd) & 0x1F

    if avail == 0:
        print("FIFO BOS", "WR", wr, "RD", rd)
    else:
        for _ in range(avail):
            led1, led2 = read_fifo()

        print(f"WR:{wr:02d} RD:{rd:02d} AV:{avail:02d} | LED1:{led1:7d} LED2:{led2:7d}")

    time.sleep(0.2)
