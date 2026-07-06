import time
import smbus


class MAX30102Reader:
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

        # Interrupt clear
        self.read(0x00)
        self.read(0x01)

        # FIFO pointers reset
        self.write(0x04, 0x00)
        self.write(0x05, 0x00)
        self.write(0x06, 0x00)

        # FIFO config
        # sample average = 4, fifo rollover enabled, almost full = 17
        self.write(0x08, 0b01011111)

        # SpO2 mode: RED + IR
        self.write(0x09, 0x03)

        # SpO2 config:
        # ADC range 4096nA, sample rate 100Hz, pulse width 411us / 18-bit
        self.write(0x0A, 0b00100111)

        # LED pulse amplitude
        self.write(0x0C, 0x3F)  # RED
        self.write(0x0D, 0x3F)  # IR

        time.sleep(0.1)

    def part_id(self):
        return self.read(0xFF)

    def available(self):
        wr = self.read(0x04)
        rd = self.read(0x06)
        return (wr - rd) & 0x1F

    def read_fifo_sample(self):
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
            red, ir = self.read_fifo_sample()

        return red, ir
