from machine import Pin
from time import sleep
p = Pin(17, Pin.OUT)

while True:
    p.value(0)
    p.value(1)
# 67khz
