from machine import I2C, Pin
from board import pin_cfg
from time import sleep
from mma7660 import MMA7660
from ws2812b import PixelDisplay

i2c1 = I2C(1, scl=Pin(pin_cfg.i2c1_scl), sda=Pin(pin_cfg.i2c1_sda))

acc = MMA7660(i2c1)
acc.on(True)

d = bytearray(3)

r = [0 for x in range(3)]

def twos_compliment(n, nbits):
    sign_bit = 1 << nbits - 1
    sign = 1 if n & sign_bit == 0 else -1
    val = n & ~sign_bit if sign > 0 else sign * ((sign_bit << 1) - n)
    return val

def thumb_filter(a):
    return a

while True:
    acc.getSample(d)
    for i in range(3):
        r[i] = twos_compliment(d[i], 6)
    print((r[0], r[1], r[2]))
    sleep(0.01)
