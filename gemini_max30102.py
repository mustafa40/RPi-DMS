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
        # Sensörü fabrika ayarlarına döndür
        self.bus.write_byte_data(self.address, 0x09, 0x40)

    def setup(self):
        # FIFO Ayarları: Örnekleme ortalaması yok (0x00)
        self.bus.write_byte_data(self.address, 0x08, 0x00)
        # Mod Ayarları: SpO2 modu aktif (Kırmızı + IR LED) (0x03)
        self.bus.write_byte_data(self.address, 0x09, 0x03)
        # LED Akım Ayarları: Akımı optimize et (~7.2mA)
        self.bus.write_byte_data(self.address, 0x0C, 0x24)
        self.bus.write_byte_data(self.address, 0x0D, 0x24)
        # FIFO Yazma/Okuma İşaretçilerini Temizle
        self.bus.write_byte_data(self.address, 0x04, 0x00)
        self.bus.write_byte_data(self.address, 0x05, 0x00)
        self.bus.write_byte_data(self.address, 0x06, 0x00)

    def read_fifo(self):
        try:
            # FIFO veri havuzundan 6 bayt oku (3 bayt Kırmızı, 3 bayt IR)
            data = self.bus.read_i2c_block_data(self.address, 0x07, 6)
            
            # Baytları 24-bitlik tam sayılara doğru şekilde birleştir
            red = (data[0] << 16) | (data[1] << 8) | data[2]
            ir = (data[3] << 16) | (data[4] << 8) | data[5]
            
            # Sadece 18-bitlik geçerli veri kısmını maskele
            return red & 0x3FFFF, ir & 0x3FFFF
        except Exception as e:
            return None, None
