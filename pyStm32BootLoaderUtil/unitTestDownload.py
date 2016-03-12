import sys
import os
import stm32BootLoader.userCommand

fin  = open('main.bin', 'rb')
b=fin.read(256)
data=''
while(b):
    data+=b
    b=fin.read(256)
print(len(data))
BL=stm32BootLoader.userCommand.USER_BootLoader('/dev/ttyUSB0')
BL.BL.begin()
BL.BL.eraseAllMemory()
BL.writeMemory('08000000',data)
