import sys
import os
import stm32BootLoader.basicCommand

fin  = open('main.bin', 'rb')
b=fin.read(256)
data=''
while(b):
    data+=b
    b=fin.read(256)

BL=stm32BootLoader.basicCommand.BootLoader('/dev/ttyUSB0')
BL.begin()
BL.writeMemory('08000000',data)
