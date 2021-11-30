import ws2812b
import utime, time
import _thread
from machine import SPI, Pin
from ssd1306 import SSD1306_SPI
import framebuf
from astronaut import frames
from board import pin_cfg
import gc

spi = SPI(1, 100000, mosi=Pin(pin_cfg.spi1_mosi), sck=Pin(pin_cfg.spi1_sck))
oled = SSD1306_SPI(128, 64, spi, Pin(pin_cfg.spi1_dc),Pin(pin_cfg.spi1_rstn), Pin(pin_cfg.spi1_cs))

# Clear the oled display in case it has junk on it.
oled.fill(0)

state = 1

def the_second_loop():
    global state
    x = -64
    fb = [framebuf.FrameBuffer(frames[fr], 64, 64, framebuf.MONO_HLSB)
          for fr in range(0, 48)]
    while True:
        for fr in range(0, 48):
            if state == 0: continue
            oled.blit(fb[fr], x, 0)
            gc.collect()
            utime.sleep_ms(40)
            if x < 128:
                x = x + 1
            else:
                x = -64
            print(x)
            oled.show()
            
_thread.start_new_thread(the_second_loop, ())

green = "#00ff00"
red = "#ff0000"
yellow = "#fff00"

while True:
    ws2812b.on_all(red)
    state = 0
    time.sleep(5)
    ws2812b.on_all(yellow)
    time.sleep(2)
    ws2812b.on_all(green)
    state = 1
    time.sleep(5)
    ws2812b.on_all(yellow)
    time.sleep(5)
