import ws2812b
from oled import oled
from button import button
from board import pin_cfg

import time
from machine import Pin
import random

def print_result(msg):
    print(msg)
    oled.text(msg,0,32)
    oled.show()

timer_start = 0

def k1_callback(pin):
    global timer_start
    timer_reaction = time.ticks_ms() - timer_start # ticks_diff
    print_result("Your reaction time was " + str(timer_reaction) + "ms")
k1 = button(pin_cfg.k1, k1_callback, trigger=Pin.IRQ_FALLING)

while True:
    ws2812b.on_all()
    time.sleep(random.uniform(3,5))
    ws2812b.off_all()
    timer_start = time.ticks_ms()
    time.sleep(10)
