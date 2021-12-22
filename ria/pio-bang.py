from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
from time import sleep

@asm_pio(set_init=PIO.OUT_LOW)
def bang():
    set(pins, 0)
    set(pins, 1) [2]

sm1 = StateMachine(1, bang, freq=10_000_000, set_base=Pin(17))

sm1.active(1)

while True:
    sleep(10)
