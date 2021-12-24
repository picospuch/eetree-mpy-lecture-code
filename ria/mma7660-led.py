from machine import I2C, Pin
from board import pin_cfg
from time import sleep
from mma7660 import MMA7660
from oled import oled
import ws2812b

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

# for i in range(64):
#     print(twos_compliment(i, 6))

def thumb_filter(a):
    return a / 23.0 * 32.0

while True:
    acc.getSample(d)
    for i in range(3):
        r[i] = twos_compliment(d[i], 6)
    print((r[0], r[1], r[2]))
    oled.fill(0)
    oled.text("(x:{0},y:{1},z:{2})".format(r[0], r[1], r[2]), 0, 10)
    oled.show()
    if r[0] < 0:
        v = -r[0]
        v = thumb_filter(v)
        ws2812b.off(3)
        ws2812b.on(9, light_value(
            int(v / 32.0 * 255.0)
        ))
    elif r[0] > 0:
        v = r[0]
        v = thumb_filter(v)
        ws2812b.off(9)
        ws2812b.on(3, light_value(
            int(v / 32.0 * 255.0)
        ))
        
    if r[1] < 0:
        v = -r[1]
        v = thumb_filter(v)
        ws2812b.off(12)
        ws2812b.on(6, light_value(
            int(v / 32.0 * 255.0)
        ))
    elif r[1] > 0:
        v = r[1]
        v = thumb_filter(v)
        ws2812b.off(6)
        ws2812b.on(12, light_value(
            int(v / 32.0 * 255.0)
        ))
    sleep(0.1)
