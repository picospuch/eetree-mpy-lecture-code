from machine import PWM, Pin
import time
from board import pin_cfg

led = PWM(Pin(pin_cfg.red_led))

led.freq(1000)

sensor_temp = machine.ADC(4)

conversion_factor = 3.3 / 65535

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    d = int((temperature - 20) * 10000)
    d = d if d > 0 else 0
    d = d if d < 65535 else 65535
    led.duty_u16(d)
    print(temperature)
    time.sleep(2)
