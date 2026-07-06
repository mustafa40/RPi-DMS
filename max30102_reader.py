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
    REG_LED1_PA = 0x0C
    REG_LED2_PA = 0x0D
 
    def __init__(self, bus=1):
        self.bus = smbus.SMBus(bus)
 
    def write_reg(self, reg, value):
        self.bus.write_byte_data(self.ADDRESS, reg, value)
 
    def read_reg(self, reg):
        return self.bus.read_byte_data(self.ADDRESS, reg)
 
    def setup(self):
        # Reset
        self.write_reg(self.REG_MODE_CONFIG, 0x40)
        time.sleep(0.2)
 
        # FIFO reset
        self.write_reg(self.REG_FIFO_WR_PTR, 0x00)
        self.write_reg(self.REG_OVF_COUNTER, 0x00)
        self.write_reg(self.REG_FIFO_RD_PTR, 0x00)
 
        # FIFO average 4 samples
        self.write_reg(self.REG_FIFO_CONFIG, 0x4F)
 
        # SpO2 mode: RED + IR
        self.write_reg(self.REG_MODE_CONFIG, 0x03)
 
        # ADC range / sample rate / pulse width
        self.write_reg(self.REG_SPO2_CONFIG, 0x27)
 
        # LED currents
        self.write_reg(self.REG_LED1_PA, 0x24)  # RED
        self.write_reg(self.REG_LED2_PA, 0x24)  # IR
 
    def read_fifo(self):
        data = self.bus.read_i2c_block_data(self.ADDRESS, self.REG_FIFO_DATA, 6)
 
        red = ((data[0] << 16) | (data[1] << 8) | data[2]) & 0x03FFFF
        ir = ((data[3] << 16) | (data[4] << 8) | data[5]) & 0x03FFFF
 
        return red, ir
