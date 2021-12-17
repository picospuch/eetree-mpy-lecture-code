from board import pin_cfg
from time import sleep
import ws2812b
from machine import ADC, Pin
from oled import oled

def light_value(l):
    return "#{0:02x}{1:02x}{2:02x}".format(l, l, l)

pot = ADC(Pin(pin_cfg.pot))
hist = [0 for i in range(128)]
while True:
    v_256 = int(pot.read_u16() * 255.0 / 65535.0)
    v_64 = int(pot.read_u16() * 63.0 / 65535.0)

    for i in range(127):
        hist[i] = hist[i + 1]
    hist[127] = v_64
    
    print(v_256)
    ws2812b.on_all(light_value(v_256))

    oled.fill(0)
    for i in range(128):
        #oled.pixel(i, hist[i], 1)
        if i >= 1:
           oled.line(i - 1, hist[i - 1], i, hist[i], 1)

    oled.show()
    sleep(0.1)
