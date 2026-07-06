import time
import smbus


class MAX30102Reader:
    ADDRESS = 0x57

    REG_INTR_STATUS_1 = 0x00
    REG_INTR_STATUS_2 = 0x01
    REG_FIFO_WR_PTR = 0x04
    REG_OVF_COUNTER = 0x05
    REG_FIFO_RD_PTR = 0x06
    REG_FIFO_DATA = 0x07
    REG_FIFO_CONFIG = 0x08
    REG_MODE_CONFIG = 0x09
    REG_SPO2_CONFIG = 0x0A
    REG_LED1_PA = 0x0C  # RED
    REG_LED2_PA = 0x0D  # IR
    REG_PART_ID = 0xFF

    def __init__(self, bus=1):
        self.bus = smbus.SMBus(bus)

    def write_reg(self, reg, value):
        self.bus.write_byte_data(self.ADDRESS, reg, value)

    def read_reg(self, reg):
        return self.bus.read_byte_data(self.ADDRESS, reg)

    def setup(self):
        self.write_reg(self.REG_MODE_CONFIG, 0x40)
        time.sleep(0.2)

        self.write_reg(self.REG_FIFO_WR_PTR, 0x00)
        self.write_reg(self.REG_OVF_COUNTER, 0x00)
        self.write_reg(self.REG_FIFO_RD_PTR, 0x00)

        self.write_reg(self.REG_FIFO_CONFIG, 0x5F)
        self.write_reg(self.REG_MODE_CONFIG, 0x03)
        self.write_reg(self.REG_SPO2_CONFIG, 0x2F)

        self.write_reg(self.REG_LED1_PA, 0x7F)
        self.write_reg(self.REG_LED2_PA, 0x7F)

        self.read_reg(self.REG_INTR_STATUS_1)
        self.read_reg(self.REG_INTR_STATUS_2)

    def available_samples(self):
        wr = self.read_reg(self.REG_FIFO_WR_PTR)
        rd = self.read_reg(self.REG_FIFO_RD_PTR)
        return (wr - rd) & 0x1F

    def read_sample(self):
        data = self.bus.read_i2c_block_data(self.ADDRESS, self.REG_FIFO_DATA, 6)

        red = ((data[0] << 16) | (data[1] << 8) | data[2]) & 0x03FFFF
        ir = ((data[3] << 16) | (data[4] << 8) | data[5]) & 0x03FFFF

        return red, ir

    def read_latest(self):
        samples = self.available_samples()

        if samples == 0:
            return None, None

        red, ir = 0, 0
        for _ in range(samples):
            red, ir = self.read_sample()

        return red, ir

    def part_id(self):
        return self.read_reg(self.REG_PART_ID)
