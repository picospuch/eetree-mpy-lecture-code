from board import pin_cfg

from machine import Pin, PWM
import time

pwm = PWM(Pin(pin_cfg.buzzer))

def pitch(frequency, duration=0):
    pwm.freq(frequency)
    pwm.duty_u16(3000)
    time.sleep_ms(duration)

while True:
    for freq in range(880, 1760, 16):
        pitch(freq, 6)
    for freq in range(1760, 880, -16):
        pitch(freq, 6)
