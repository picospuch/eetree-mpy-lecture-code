import ws2812b
from button import k1, k2

def setup():
    global n
    n = 1
    pass

def loop():
    global n
    if k1.value() == True:
        ws2812b.off(n)
        n = n + 1
    if k2.value() == True:
        ws2812b.off(n)
        n = n - 1
    n = (n - 1) % 12 + 1
    ws2812b.on(n)

setup()
while True:
    loop()
