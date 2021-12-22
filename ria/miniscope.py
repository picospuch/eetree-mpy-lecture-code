import time
from machine import ADC, Pin
from board import pin_cfg
from oled import oled

adc = ADC(Pin(pin_cfg.adc1))

sample_buf = bytearray(256)

def sample_capture():
    for i in range(128):
        d = adc.read_u16()
        sample_buf[i * 2] = d & 0xff
        sample_buf[i * 2 + 1] = (d >> 8) & 0xff
        time.sleep_us(20) # 440hz, 2500us/div

def thumb_filter(d):
    d = (d - (65535 / 2)) * 4 + 65535 / 2
    if d < 0:
        d = 0
    if d > 65535:
        d = 65535
    return d / 65535 * 63

def sample_read(i):
    d = sample_buf[i * 2] + (sample_buf[i * 2 + 1] << 8)
    return int(thumb_filter(d))

def display():
    oled.fill(0)
    for i in range(128):
        if i >= 1:
            oled.line(i - 1, sample_read(i - 1), i, sample_read(i), 1)
    oled.show()
    
while True:
    sample_capture()
    display()

