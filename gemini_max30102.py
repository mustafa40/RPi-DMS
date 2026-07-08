import smbus
import time

class MAX30102:
    def __init__(self, address=0x57, bus=1):
        self.bus = smbus.SMBus(bus)
        self.address = address
        self.reset()
        time.sleep(0.1)
        self.setup()

    def reset(self):
        self.bus.write_byte_data(self.address, 0x09, 0x40)

    def setup(self):
        # FIFO Konfigürasyonu
        self.bus.write_byte_data(self.address, 0x08, 0x00)
        # SpO2 Modu aktif (Kırmızı ve IR LED)
        self.bus.write_byte_data(self.address, 0x09, 0x03)
        # LED Akım Ayarları (~7.2mA)
        self.bus.write_byte_data(self.address, 0x0C, 0x24)
        self.bus.write_byte_data(self.address, 0x0D, 0x24)
        # FIFO İşaretçilerini Sıfırla
        self.bus.write_byte_data(self.address, 0x04, 0x00)
        self.bus.write_byte_data(self.address, 0x05, 0x00)
        self.bus.write_byte_data(self.address, 0x06, 0x00)

    def read_fifo(self):
        try:
            # FIFO verisini oku (6 bayt: 3 RED, 3 IR)
            data = self.bus.read_i2c_block_data(self.address, 0x07, 6)
            red = (data[0] << 16) | (data[1] << 8) | data[2]
            ir = (data[3] << 16) | (data[4] << 8) | data[5]
            return red, ir
        except:
            return None, None
