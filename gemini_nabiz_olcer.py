import time
import math
from max30102 import MAX30102

sensor = MAX30102()
BUFFER_SIZE = 100
ir_buffer = []
red_buffer = []

print("Sensör hazır. Lütfen parmağınızı yerleştirin...")

def mean(data):
    return sum(data) / len(data)

def rms(data, data_mean):
    return math.sqrt(sum((x - data_mean) ** 2 for x in data) / len(data))

def calculate_bpm_spo2(red_data, ir_data):
    ir_mean = mean(ir_data)
    red_mean = mean(red_data)
    ir_ac = [x - ir_mean for x in ir_data]
    
    # Sıfır geçiş tespiti ile Nabız (BPM)
    zero_crossings = 0
    for i in range(len(ir_ac) - 1):
        if (ir_ac[i] >= 0 and ir_ac[i+1] < 0) or (ir_ac[i] < 0 and ir_ac[i+1] >= 0):
            zero_crossings += 1
            
    if zero_crossings < 2:
        return 0, 0
        
    total_seconds = len(ir_data) * 0.01 
    hz = (zero_crossings / 2) / total_seconds
    bpm = hz * 60
    
    # SpO2 için R Oranı
    red_rms_val = rms(red_data, red_mean)
    ir_rms_val = rms(ir_data, ir_mean)
    
    if ir_rms_val == 0 or ir_mean == 0:
        return int(bpm), 0
        
    R = (red_rms_val / red_mean) / (ir_rms_val / ir_mean)
    spo2 = 110 - 25 * R
    spo2 = max(0, min(100, spo2))
    
    return int(bpm), int(spo2)

try:
    while True:
        red, ir = sensor.read_fifo()
        if red is not None and ir is not None:
            if ir < 40000:
                print("⚠️ Parmak algılanmadı! Lütfen parmağınızı koyun.", end="\r")
                ir_buffer.clear()
                red_buffer.clear()
                time.sleep(0.5)
                continue
                
            ir_buffer.append(ir)
            red_buffer.append(red)
            
            if len(ir_buffer) >= BUFFER_SIZE:
                bpm, spo2 = calculate_bpm_spo2(red_buffer, ir_buffer)
                if 45 <= bpm <= 160 and 80 <= spo2 <= 100:
                    print(f"❤️ Nabız: {bpm} BPM | 🩸 Oksijen: %{spo2}      ")
                else:
                    print("🔄 Sinyal kalitesi zayıf, sabit bekleyin...", end="\r")
                
                ir_buffer = ir_buffer[30:]
                red_buffer = red_buffer[30:]
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\n⏹️ Ölçüm sonlandırıldı.")
