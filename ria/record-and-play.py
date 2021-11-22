import time
from button import k1, k2
from machine import ADC, Pin
from board import pin_cfg

adc = ADC(Pin(pin_cfg.adc1))

sample = bytearray(40000)
while True:
    if k1.value() == True:
        time.sleep_ms(100)
        for i in range(0, 20000):
            d = adc.read_u16()
            sample[i * 2] = d
            sample[i * 2 + 1] = d >> 8
            time.sleep_us(60)
        print("20000 sampled.")
    if k2.value() == True:
        for i in range(0, 200):
            d = sample[i * 2] + sample[i * 2 + 1] << 8
            print(d)
