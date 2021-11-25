from board import pin_cfg
import time
from machine import Pin
import led
import oled
import ws2812b

while True:
    time.sleep(1)
    oled.oled.fill(1)
    oled.oled.show()
    led.r.on()
    led.g.on()
    led.b.on()
    led.y.on()
    for i in range(1, 13):
        ws2812b.on(i)
    time.sleep(1)
    oled.oled.fill(0)
    oled.oled.show()
    led.r.off()
    led.g.off()
    led.b.off()
    led.y.off()
    for i in range(1, 13):
        ws2812b.off(i)
