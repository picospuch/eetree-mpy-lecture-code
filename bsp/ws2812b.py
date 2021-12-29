import array, time, math
from machine import Pin
import rp2

LED_COUNT = 12 # number of LEDs in ring light
PIN_NUM = 18 # pin connected to ring light
brightness = 1.0 # 0.1 = darker, 1.0 = brightest

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT,
             autopull=True, pull_thresh=24) # PIO configuration
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

state_mach = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))
state_mach.active(1)

pixel_array = array.array("I", [0 for _ in range(LED_COUNT)])

def update_pix(brightness_input=brightness): # dimming colors and updating state machine (state_mach)
    dimmer_array = array.array("I", [0 for _ in range(LED_COUNT)])
    for ii,cc in enumerate(pixel_array):
        r = int(((cc >> 8) & 0xFF) * brightness_input) # 8-bit red dimmed to brightness
        g = int(((cc >> 16) & 0xFF) * brightness_input) # 8-bit green dimmed to brightness
        b = int((cc & 0xFF) * brightness_input) # 8-bit blue dimmed to brightness
        dimmer_array[ii] = (g<<16) + (r<<8) + b # 24-bit color dimmed to brightness
    state_mach.put(dimmer_array, 8) # update the state machine with new colors
    time.sleep_ms(10)

def set_24bit(ii, color): # set colors to 24-bit format inside pixel_array
    color = hex_to_rgb(color)
    pixel_array[ii] = (color[1]<<16) + (color[0]<<8) + color[2] # set 24-bit color
    
def hex_to_rgb(hex_val):
    return tuple(int(hex_val.lstrip('#')[ii:ii+2],16) for ii in (0,2,4))

def on(n, color = "#ffffff"):
    if not ((n >= 1 and n <= 12) and isinstance(n, int)):
        print("arg error")
        return
    set_24bit((n - 1) % 12, color)
    update_pix()
    
def off(n, color = "#000000"):
    if not ((n >= 1 and n <= 12) and isinstance(n, int)):
        print("arg error")
        return
    set_24bit((n - 1) % 12, color)
    update_pix()

def on_all(color = "#ffffff"):
    for i in range(0,12):
        set_24bit(i, color)
    update_pix()

def off_all(color = "#000000"):
    for i in range(0,12):
        set_24bit(i, color)
    update_pix()

def light_value(l):
    if l > 255: l = 255
    elif l < 0: l = 0
    return "#{0:02x}{1:02x}{2:02x}".format(l, l, l)

class PixelDisplay():
    def __init__(self):
        self.pixel_array = array.array("I", [0 for _ in range(12)])

    def set_color(self, n, color):
        """set the color of pixel 'n
        n - 1...12
        color - color tuple"""
        self.pixel_array[(n - 1) % LED_COUNT] = (color[1]<<16) + (color[0]<<8) + color[2]

    def get_color(self, n):
        v = self.pixel_array[(n - 1) % LED_COUNT]
        return ((v >> 8) & 0xff, (v >> 16) & 0xff, v & 0xff)
    
    def fill(self, c):
        for i in range(1, LED_COUNT + 1):
            self.set_color(i, c)

    def dim(self, brightness_input = 1, n = None):
        if n is not None:
            cc = self.pixel_array[n - 1]
            r = int(((cc >> 8) & 0xFF) * brightness_input) # 8-bit red dimmed to brightness
            g = int(((cc >> 16) & 0xFF) * brightness_input) # 8-bit green dimmed to brightness
            b = int((cc & 0xFF) * brightness_input) # 8-bit blue dimmed to brightness
            self.pixel_array[n - 1] = (g<<16) + (r<<8) + b # 24-bit color dimmed to brightness
        else:
            for ii,cc in enumerate(self.pixel_array):
                r = int(((cc >> 8) & 0xFF) * brightness_input) # 8-bit red dimmed to brightness
                g = int(((cc >> 16) & 0xFF) * brightness_input) # 8-bit green dimmed to brightness
                b = int((cc & 0xFF) * brightness_input) # 8-bit blue dimmed to brightness
                self.pixel_array[ii] = (g<<16) + (r<<8) + b # 24-bit color dimmed to brightness
            
    def rainbow(self, offset = 0):
        for i in range(1, LED_COUNT + 1):
            rc_index = (i * 256 // LED_COUNT) + offset
            self.set_color(i, wheel(rc_index & 255))

    def render(self):
        state_mach.put(self.pixel_array, 8)

def wheel(pos):
  """Input a value 0 to 255 to get a color value.
  The colours are a transition r - g - b - back to r."""
  if pos < 0 or pos > 255:
    return (0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3)
