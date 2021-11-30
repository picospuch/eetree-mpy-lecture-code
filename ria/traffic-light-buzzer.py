import time
import ws2812b
from button import k1
from machine import PWM, Pin
from board import pin_cfg

pwm = PWM(Pin(pin_cfg.buzzer))

def pitch(frequency, duration=0):
    pwm.freq(frequency)
    pwm.duty_u16(3000)
    time.sleep_ms(duration)

def red_light():
    for i in range(1, 13):
        ws2812b.on(i, "#ff0000")    
def yellow_light():
    for i in range(1, 13):
        ws2812b.on(i, "#ffff00")
def green_light():
    for i in range(1, 13):
        ws2812b.on(i, "#00ff00")

while True:
    if k1.value() == True:
        red_light()
        print("+5 start")
        for i in range(10):
            for freq in range(880, 1760, 16):
                pitch(freq, 6)
            for freq in range(1760, 880, -16):
                pitch(freq, 6)
        print("+5 end")
        pwm.deinit()

    red_light()
    time.sleep(5)
    yellow_light()
    time.sleep(2)
    green_light()
    time.sleep(5)
    yellow_light()
    time.sleep(2)
