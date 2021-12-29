from array import array
from utime import sleep_us
from math import pi,sin,exp,sqrt,floor
from machine import Pin
from random import random
import test_sound
import dac

hiz = Pin(19, Pin.IN)

i = 0
while True:
    dac.output(test_sound.blob[i])
    i = i + 1
    #sleep_us(1)
