from board import pin_cfg

from machine import Pin, PWM
from time import sleep

# pwm = freq + duty
led = PWM(Pin(pin_cfg.red_led))

led.freq(1000)

n = 0
while True:
    if n <= 0:
        a = 1000
    elif n >= 10000:
        a = -1000
    n = n + a
    led.duty_u16(n)
    sleep(0.1)
