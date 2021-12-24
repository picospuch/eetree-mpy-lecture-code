import ws2812b as wb
from machine import RTC, ADC, Pin
from board import pin_cfg
from time import sleep, sleep_us
from astronaut import frames
from oled import oled
import framebuf
import freesans20
from writer import Writer
import array
from fft import fft, f_peaks, f_peaks_amp

rtc = RTC()

peak = 255

class PixelDisplay():
    def __init__(self, wb):
        self.pixel_array = array.array("I", [0 for _ in range(12)])

    def set_color(self, n, color):
        self.pixel_array[(n - 1) % 12] = (color[1]<<16) + (color[0]<<8) + color[2]

    def get_color(self, n):
        v = self.pixel_array[(n - 1) % 12]
        return ((v >> 8) & 0xff, (v >> 16) & 0xff, v & 0xff)
    
    def fill(self, c):
        a = self.pixel_array
        for i in range(12):
            a[i] = c

    def pixels_show(self, brightness_input=1):
        for ii,cc in enumerate(self.pixel_array):
            r = int(((cc >> 8) & 0xFF) * brightness_input) # 8-bit red dimmed to brightness
            g = int(((cc >> 16) & 0xFF) * brightness_input) # 8-bit green dimmed to brightness
            b = int((cc & 0xFF) * brightness_input) # 8-bit blue dimmed to brightness
            self.pixel_array[ii] = (g<<16) + (r<<8) + b # 24-bit color dimmed to brightness
            
    def render(self):
        wb.state_mach.put(self.pixel_array, 8)

class OledTime():
    def __init__(self, oled, frames):
        self.oled = oled
        self.frames = frames
        self.oled.fill(0)
        self.i = len(frames) - 1
        self.wri = Writer(oled, freesans20)

    def show_date(self, year, month):
        self.y = year
        self.m = month
        
    def draw(self):
        if self.i == 0:
            self.i = len(frames) - 1
        else:
            self.i = self.i - 1
        fb = framebuf.FrameBuffer(self.frames[self.i], 64, 64, framebuf.MONO_HLSB)
        
        self.oled.blit(fb, 0, 0, 0)

        self.wri.set_textpos(oled, 10, 70)
        self.wri.printstring(str(self.y))
        self.wri.set_textpos(oled, 30, 85)
        self.wri.printstring(str(self.m))

class Ws2812Time():
    def __init__(self, pd):
        self.pd = pd
        self.h = 0
        self.m = 0
        self.s = 0
        
    def show_time(self, h, m, s):
        h_tmp = h
        m_tmp = m
        s_tmp = s

        self.h = (h_tmp - 1) % 12 + 1
        self.m = (int(m_tmp / 5) - 1) % 12 + 1
        self.s = (int(s_tmp / 5) - 1) % 12 + 1

    def draw(self):
        pd.set_color(self.h, (0xff, 0, 0))
        pd.set_color(self.m, (0, 0xff, 0))
        pd.set_color(self.s, (0, 0, 0xff))

class SoundMeter():
    def __init__(self, oled):
        self.oled = oled
        self.adc = ADC(Pin(pin_cfg.adc1))
        self.buf = array.array("H", [0 for _ in range(180)])
        self.gbuf = bytearray(128 * 64)
        self.fb = framebuf.FrameBuffer(self.gbuf, 128, 64, framebuf.MONO_HLSB)
        self.pos = 0
        
    def capture(self):
        buf = self.buf
        adc = self.adc
        for i in range(128):
            d = adc.read_u16()
            buf[i] = d
            sleep_us(142)

    def shift_buffer(self):
        buf = self.buf
        for i in range(180 - 6):
            buf[i] = buf[i + 6]
            
    def capture_tick(self):
        buf = self.buf
        adc = self.adc

        self.shift_buffer()
        
        # capture window
        for i in range(174, 180):
            buf[i] = self.thumb_filter(adc.read_u16())
            sleep_us(6)

    def thumb_filter(self, d):
        if d < 0:
            d = 0
        if d > 65535:
            d = 65535
        return int(d / 65535 * 63)

    def fft(self):
        global peak
        v = memoryview(self.buf)
        fft(v[30:158], 128, 100)
        #print(f_peaks)
        #print(f_peaks_amp)
        peak = int(f_peaks_amp[1])
        if peak < 30:
            peak = 0

    def draw(self):
        buf = self.buf
        fb = self.fb

        fb.fill(0)
        for i in range(128):
            if i >= 1:
                fb.line(i - 1, buf[i - 1 + 30], i, buf[i + 30], 1)

        self.oled.blit(fb, 0, 20, 0)

class BreathingAnimation():
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    yellow = (255,255,0)
    cyan = (0,255,255)
    white = (255,255,255)
    blank = (0,0,0)
    colors = [blue,yellow,cyan,red,green,white]
    breath_amps = [i for i in range(0,255,8)]
    
    def __init__(self, pd):
        self.pd = pd
        self.ai = 0
        self.ci = 0
        pass

    def update_breath_amps(self):
        #self.breath_amps = [i for i in range(0,peak,8)]
        #self.breath_amps.extend([i for i in range(peak,-1,-8)])
        self.breath_amps = [i for i in range(peak, -1, -8)]

    def breathing_led(self):
        pd = self.pd

        al = len(self.breath_amps)        
        c = self.colors[self.ci]
        
        ai = al - 1 if self.ai > al - 1 else self.ai
        if ai >= 0:
            d = self.breath_amps[ai]/255
        else:
            d = 0
        #d = peak/255
        
        for i in range(12):
            pd.set_color(i + 1, c)
        if d == 0:   
            self.ci = (self.ci + 1) % len(self.colors)

        pd.pixels_show(d)

        if al > 0:
            self.ai = (self.ai + 1) % al

    def draw(self):        
        pass
        

pd = PixelDisplay(wb)
ws2812_time = Ws2812Time(pd)
oled_time = OledTime(oled, frames)
breathing_animation = BreathingAnimation(pd)
sound_meter = SoundMeter(oled)

tick = 0
while True:
    oled.fill(0)

    dt_tuple = rtc.datetime()

    year = dt_tuple[0]
    month = dt_tuple[1]
    
    h = dt_tuple[4] # r
    m = dt_tuple[5] # g
    s = dt_tuple[6] # b

    oled_time.show_date(year, month)

    breathing_animation.breathing_led()
    # pd.set_color(tick % 12, (0xff, 0xef, 0x12))
    ws2812_time.show_time(h, m, s)
    sound_meter.capture_tick()

    if tick % 8 == 0:
        sound_meter.fft()
        breathing_animation.update_breath_amps()

    # drawing
    oled_time.draw()
    sound_meter.draw()
    breathing_animation.draw()
    ws2812_time.draw()

    # rendering
    oled.show()
    pd.render()

    tick = (tick + 1) % 65536
    sleep(0.04) # fps = 25
