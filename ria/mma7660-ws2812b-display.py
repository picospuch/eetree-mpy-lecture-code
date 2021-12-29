from machine import I2C, Pin
from board import pin_cfg
from time import sleep
from mma7660 import MMA7660
from oled import oled
from ws2812b import PixelDisplay
from p_math import sin, cos, pi
from math import atan

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
    if a > 15: a = 15
    return a / 15

def low_pass_filter(a, la):
    k = 0.3
    return a * k + la * (1 - k)

pd = PixelDisplay()

v = 0


def comet(pd, n, c, t):
    t = t // 5
    l = 6
    gap = 10

    cur = t % l
    for i in range(l):
        ln = (n - (l - 1) + i + 12 - 1) % 12 + 1
        if cur == 0:
            pd.set_color(ln, (0, 0, 0))
        if cur == i:
            pd.set_color(ln, c)
        pd.dim(0.8, ln)

def comet_2way(pd, n, c, t):
    t = t // 10
    
    l = 5

    t = t % ( l + l )

    if t < l:
        f = t
    else:
        f = l - 1
    
    gap = 10

    cur = f % l
    for i in range(l):
        ln = (n - (l - 1) + i + 12 - 1) % 12 + 1
        lnn = (n + l - i - 1 - 1) % 12 + 1
        if cur == 0:
            pd.set_color(ln, (0, 0, 0))
            pd.set_color(lnn, (0, 0, 0))
        if cur == i:
            pd.set_color(ln, c)
            pd.set_color(lnn, c)
        pd.dim(0.85, ln)
        pd.dim(0.85, lnn)

last_z = 0
def z_filter(z):
    global last_z
    z = z if z > 0 else -z
    if z > 23:
        z = 23
    z = z / 23
    lpf = low_pass_filter(z, last_z)
    last_z = z
    return lpf

def radian(x, y):
    if x == 0: x = 0.0001
    r = atan(y / x)
    r = r + pi if x < 0 else r
    r = r + pi if y < 0 else r
    return r

ra = 0

tolerant = 0.08

tick = 0
while True:
    acc.getSample(d)
    for i in range(3):
        r[i] = twos_compliment(d[i], 6)
    #print((r[0], r[1], r[2]))

    last_ra = ra
    ra = radian(r[0], r[1])
    #ra = low_pass_filter(ra, last_ra)

    if z_filter(r[2]) > 0.86:
        pd.fill((255,255,255))
    else:
        for i in range(12):
            rrr = 2 * pi / 12 * ( (3 - i) % 12)
            if ra > rrr * (1 - tolerant) and ra < rrr * (1 + tolerant):
                comet_2way(pd, (i - 1) % 12 + 1, (255,0,0), tick)
                #pd.fill((0, 0, 0))
                #pd.set_color((i - 1) % 12 + 1, (255,0,0))
        
    # pd.dim(v, 9)
    # pd.dim(v * 2 / 3, 10)
    # pd.dim(v * 2 / 3, 8)
    # pd.dim(v * 1 / 3, 7)
    # pd.dim(v * 1 / 3, 11)

    pd.render()
    tick = (tick + 1) % 65536
    sleep(0.01)
