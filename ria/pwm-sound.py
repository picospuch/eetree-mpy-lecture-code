# Arbitrary waveform generator for Rasberry Pi Pico
# Requires 8-bit R2R DAC on pins 0-7. Works for R=1kOhm
# Achieves 125Msps when running 125MHz clock
# Rolf Oldeman, 13/2/2021. CC BY-NC-SA 4.0 licence
# tested with rp2-pico-20210205-unstable-v1.14-8-g1f800cac3.uf2
from machine import Pin,mem32
from rp2 import PIO, StateMachine, asm_pio
from array import array
from utime import sleep
from math import pi,sin,exp,sqrt,floor
from uctypes import addressof
from random import random
import test_sound

## DMA Register File
DMA_BASE=0x50000000
CH0_READ_ADDR  =DMA_BASE+0x000
CH0_WRITE_ADDR =DMA_BASE+0x004
CH0_TRANS_COUNT=DMA_BASE+0x008
CH0_CTRL_TRIG  =DMA_BASE+0x00c
CH0_AL1_CTRL   =DMA_BASE+0x010
CH1_READ_ADDR  =DMA_BASE+0x040
CH1_WRITE_ADDR =DMA_BASE+0x044
CH1_TRANS_COUNT=DMA_BASE+0x048
CH1_CTRL_TRIG  =DMA_BASE+0x04c
CH1_AL1_CTRL   =DMA_BASE+0x050
CHAN_ABORT     =DMA_BASE+0x444

## PIO Register File
PIO0_BASE      =0x50200000
PIO0_TXF0      =PIO0_BASE+0x10
PIO0_SM0_CLKDIV=PIO0_BASE+0xc8

#state machine that just pushes bytes to the pins
@asm_pio(out_init=(PIO.OUT_HIGH, autopull=True, pull_thresh=32)
def stream():
    out(pins,1)

sm = StateMachine(0, stream, freq=8000 * 256, out_base=Pin(19))
sm.active(1)

### reset
sm.restart()
mem32[CH0_AL1_CTRL]=0
mem32[CH1_AL1_CTRL]=0
mem32[CHAN_ABORT]= 0xffff
###~reset

#2-channel chained DMA. channel 0 does the transfer, channel 1 reconfigures
p=array('I',[0]) #global 1-element array
def startDMA(ar,nword):
    #print("start startdma")
    #first disable the DMAs to prevent corruption while writing
    mem32[CH0_AL1_CTRL]=0
    mem32[CH1_AL1_CTRL]=0
    #setup first DMA which does the actual transfer
    mem32[CH0_READ_ADDR]=addressof(ar)
    mem32[CH0_WRITE_ADDR]=PIO0_TXF0
    mem32[CH0_TRANS_COUNT]=nword
    IRQ_QUIET=0x1 #do not generate an interrupt
    TREQ_SEL=0x00 #wait for PIO0_TX0
    CHAIN_TO=1    #start channel 1 when done
    RING_SEL=0
    RING_SIZE=0   #no wrapping
    INCR_WRITE=0  #for write to array
    INCR_READ=1   #for read from array
    DATA_SIZE=2   #32-bit word transfer
    HIGH_PRIORITY=1
    EN=1
    CTRL0=(IRQ_QUIET<<21)|(TREQ_SEL<<15)|(CHAIN_TO<<11)|(RING_SEL<<10)|(RING_SIZE<<9)|(INCR_WRITE<<5)|(INCR_READ<<4)|(DATA_SIZE<<2)|(HIGH_PRIORITY<<1)|(EN<<0)
    mem32[CH0_AL1_CTRL]=CTRL0
    #setup second DMA which reconfigures the first channel
    p[0]=addressof(ar)
    mem32[CH1_READ_ADDR]=addressof(p)
    mem32[CH1_WRITE_ADDR]=CH0_READ_ADDR
    mem32[CH1_TRANS_COUNT]=1
    IRQ_QUIET=0x1 #do not generate an interrupt
    TREQ_SEL=0x3f #no pacing
    CHAIN_TO=0    #start channel 0 when done
    RING_SEL=0
    RING_SIZE=0   #no wrapping
    INCR_WRITE=0  #single write
    INCR_READ=0   #single read
    DATA_SIZE=2   #32-bit word transfer
    HIGH_PRIORITY=1
    EN=1
    CTRL1=(IRQ_QUIET<<21)|(TREQ_SEL<<15)|(CHAIN_TO<<11)|(RING_SEL<<10)|(RING_SIZE<<9)|(INCR_WRITE<<5)|(INCR_READ<<4)|(DATA_SIZE<<2)|(HIGH_PRIORITY<<1)|(EN<<0)
    mem32[CH1_CTRL_TRIG]=CTRL1
    #print("end startdma")

startDMA(test_sound.blob, int(10000/4))

while True:
    pass
