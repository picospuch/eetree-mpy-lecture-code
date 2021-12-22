import ws2812b as wb
from machine import RTC
from time import sleep

rtc = RTC()

h = m = s = 0
h_invalid = m_invalid = s_invalid = True
while True:
    dt_tuple = rtc.datetime()
    
    h_tmp = dt_tuple[4] # r
    m_tmp = dt_tuple[5] # g
    s_tmp = dt_tuple[6] # b

    h_tmp = (h_tmp - 1) % 12 + 1
    m_tmp = (int(m_tmp / 5) - 1) % 12 + 1
    s_tmp = (int(s_tmp / 5) - 1) % 12 + 1

    if h != h_tmp:
        last_h = h
        h = h_tmp
        h_invalid = True
    if m != m_tmp:
        last_m = m
        m = m_tmp
        m_invalid = True
    if s != s_tmp:
        last_s = s
        s = s_tmp
        s_invalid = True
    
    if last_s == h or last_m == h:
        h_invalid = True
    
    if last_s == m:
        m_invalid = True
    
    if h_invalid:
        h_invalid = False
        if last_h != 0:
            wb.off(last_h)
        wb.on(h, "#ff0000")
    if m_invalid:
        m_invalid = False
        if last_m != h and last_m != 0:
            wb.off(last_m)
        wb.on(m, "#00ff00")
    if s_invalid:
        s_invalid = False
        if last_s != h and last_s != m and last_s != 0:
            wb.off(last_s)
        wb.on(s, "#0000ff")
    
    sleep(0.1)
