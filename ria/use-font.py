from oled import oled
import font6
import freesans20
from writer import Writer
from machine import RTC

rtc = RTC()

wri = Writer(oled, freesans20)

while True:
    hour = rtc.datetime()[4]
    minute = rtc.datetime()[5]
    wri.set_textpos(oled, 0, 0)
    wri.printstring(str(hour) + ":" + str(minute))
    oled.show()
