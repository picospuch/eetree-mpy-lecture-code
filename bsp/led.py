from board import pin_cfg
import time
from machine import Pin

r = Pin(pin_cfg.red_led, Pin.OUT)
g = Pin(pin_cfg.green_led, Pin.OUT)
b = Pin(pin_cfg.blue_led, Pin.OUT)
y = Pin(pin_cfg.yellow_led, Pin.OUT)
