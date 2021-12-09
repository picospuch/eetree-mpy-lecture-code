# 此实例采集温度信息并用来控制LED

from board import pin_cfg

from machine import ADC, PWM, Pin
from time import sleep

# 初始化
led = PWM(Pin(pin_cfg.red_led))
led.freq(1000)

sensor_temp = ADC(4)

conversion_factor = 3.3 / 65535

# 主循环
while True:
    # reading 单位V
    reading = sensor_temp.read_u16() * conversion_factor
    
    temperature = 27 - (reading - 0.706)/0.001721
    
    # filter function
    d = int((temperature - 20) * 10000)
    d = d if d > 0 else 0
    d = d if d < 65535 else 65535
    
    # 控制led占空比
    led.duty_u16(d)
    
    print(temperature)
    
    sleep(2)
