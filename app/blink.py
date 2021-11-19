from board import pin_cfg
import time
import utime
from machine import Pin

while True:
    r = Pin(pin_cfg.red_led, Pin.OUT)
    r.on()
    time.sleep(1)
    r.off()
    time.sleep(1)
