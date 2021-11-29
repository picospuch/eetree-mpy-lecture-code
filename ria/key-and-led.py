from button import k1, k2
from board import pin_cfg
from led import r
import time

def toggle_led():
    if r.value() == 1:
        r.off()
    else:
        r.on()
    
while True:
    # 获得按键状态
    if k1.value() == True:
        # 根据按键状态控制LED on/off
        toggle_led()
