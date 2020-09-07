#!/usr/bin/env python
import RPi.GPIO as GPIO
import os
import mmap
import time
import ctypes

pix = [0,0,0]

fd = os.open("/dev/mem", os.O_SYNC | os.O_RDWR)
mem = mmap.mmap(fd, mmap.PAGESIZE, flags=mmap.MAP_SHARED, offset=0x3F200000)
os.close(fd)

v = ctypes.c_uint32.from_buffer(mem, 0x8).value
v &= ~(0b111 << 3)
v |= 0b001 << 3
ctypes.c_uint32.from_buffer(mem, 0x8).value |= v



GPIO.RPI_INFO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ch = [27,22,23,24,20,21]
chCLK = [20,21]
chDAT = [23,24]
chLAT = [27,22]
GPIO.setup(ch, GPIO.OUT)
state = True

C1 = (1 << chCLK[0]) | (1 << chCLK[1])
D1 = (1 << chDAT[0]) | (1 << chDAT[1])
L1 = (1 << chLAT[0]) | (1 << chLAT[1])

mass = [D1,D1,D1]
mass0 = [D1,D1,D1]
fpix = [8,10,105]
ctypes.c_uint32.from_buffer(mem, 0x28).value = D1 | L1 | C1
ctypes.c_uint32.from_buffer(mem, 0xC1).value = C1
ctypes.c_uint32.from_buffer(mem, 0x28).value = C1

try:
  while True:
    i = 0
    for PIX in range(0,128):
      ctypes.c_uint32.from_buffer(mem, 0x28).value = L1 | C1
      ii = 0
      for D in mass:
          if i < fpix[ii]:
            ctypes.c_uint32.from_buffer(mem, 0x1C).value = D
            ctypes.c_uint32.from_buffer(mem, 0x28).value = D ^ D1
          else:
             ctypes.c_uint32.from_buffer(mem, 0x28).value = D1
             ctypes.c_uint32.from_buffer(mem, 0x1C).value = C1
          ctypes.c_uint32.from_buffer(mem, 0x28).value = C1
          ii += 1
      ctypes.c_uint32.from_buffer(mem, 0x1C).value = L1
      i += 1

#    for PIX in range(0,15):
#      ctypes.c_uint32.from_buffer(mem, 0x28).value = L1
#      for D in mass0:
#        ctypes.c_uint32.from_buffer(mem, 0x28).value = D
#        ctypes.c_uint32.from_buffer(mem, 0x1C).value = C1
#        ctypes.c_uint32.from_buffer(mem, 0x28).value = C1
#      ctypes.c_uint32.from_buffer(mem, 0x1C).value = L1

except KeyboardInterrupt:
    pass

mem.close()
             
