import time
import smbus


class MAX30102:
    ADDRESS = 0x57

    def __init__(self, bus=1):
        self.bus = smbus.SMBus(bus)

    def write(self, reg, val):
        self.bus.write_byte_data(self.ADDRESS, reg, val)

    def read(self, reg):
        return self.bus.read_byte_data(self.ADDRESS, reg)

    def setup(self):
        # Reset
        self.write(0x09, 0x40)
        time.sleep(0.2)

        # Clear interrupts
        self.read(0x00)
        self.read(0x01)

        # FIFO reset
        self.write(0x04, 0x00)
        self.write(0x05, 0x00)
        self.write(0x06, 0x00)

        # FIFO config: sample avg 4, rollover enabled
        self.write(0x08, 0x4F)

        # SpO2 mode
        self.write(0x09, 0x03)

        # ADC range high, sample rate 100Hz, pulse width 411us
        self.write(0x0A, 0x27)

        # LED currents - güçlü
        self.write(0x0C, 0xFF)  # RED
        self.write(0x0D, 0xFF)  # IR

        time.sleep(0.1)

    def part_id(self):
        return self.read(0xFF)

    def available(self):
        wr = self.read(0x04)
        rd = self.read(0x06)
        return (wr - rd) & 0x1F

    def read_sample(self):
        data = self.bus.read_i2c_block_data(self.ADDRESS, 0x07, 6)

        red = ((data[0] << 16) | (data[1] << 8) | data[2]) & 0x03FFFF
        ir = ((data[3] << 16) | (data[4] << 8) | data[5]) & 0x03FFFF

        return red, ir

    def read_latest(self):
        count = self.available()

        if count == 0:
            return None, None

        red, ir = 0, 0
        for _ in range(count):
            red, ir = self.read_sample()

        return red, ir
