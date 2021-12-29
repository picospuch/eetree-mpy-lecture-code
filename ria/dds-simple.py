from array import array
from utime import sleep_us, sleep_ms
from math import pi,sin,exp,sqrt,floor
from uctypes import addressof
from random import random
import dac

i = 0
h = 255
l = 0
v = l
# 100ms
while True:
    v = h if v == l else l
    dac.output(v)
    i = i + 1
    sleep_ms(50)
