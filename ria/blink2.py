from board import pin_cfg
from machine import Pin
import time

g = Pin(pin_cfg.green_led, Pin.OUT)

while True:
    time.sleep(0.1)
    g.on()
    time.sleep(0.1)
    g.off()
