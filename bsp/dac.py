### dac.py
from rp2 import PIO, StateMachine, asm_pio
from machine import Pin,mem32

#state machine that just pushes bytes to the pins
@asm_pio(out_init=(PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH),
         out_shiftdir=PIO.SHIFT_RIGHT, autopull=True, pull_thresh=8)
def stream():
    out(pins,8)

sm = StateMachine(0, stream, freq=100_000, out_base=Pin(0))
sm.active(1)

def output(i):
    sm.put(i)
