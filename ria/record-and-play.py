import time
from button import k1, k2
from machine import ADC, Pin
from board import pin_cfg
from time import sleep_us
import dac

hiz = Pin(19, Pin.IN)
adc = ADC(Pin(pin_cfg.adc1))

# sample rate: 8000hz, 3s, 24000 samples
sample = bytearray(24000)
while True:
    if k1.value() == True:
        time.sleep_ms(100)
        for i in range(0, 24000):
            d = (((adc.read_u16() - 32768) * 16) + 32768) * 256 // 65536
            sample[i] = d & 0xff
            sleep_us(125)
        print("80000 sampled.")
    if k2.value() == True:
        for i in range(0, 24000):
            dac.output(sample[i])
            sleep_us(125)
        print("80000 outputed.")
