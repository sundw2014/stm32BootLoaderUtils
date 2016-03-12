# -*- coding:utf-8 -*-

'provide some basic operation including read, write, erase ...'
__author__ = 'sundw2014'
import stm32BootLoader.basicCommand,struct

class  USER_BootLoader:
    def __init__(self,serPath):
        self.BL=stm32BootLoader.basicCommand.BootLoader(serPath)

    def writeMemory(self , address , data):         #address is like 'aabbccdd'
        if(not self.BL.ready):
            if(not self.BL.begin()):
                print('start target failed\r\n')
                return False

        address = struct.unpack('>L',address.decode('hex'))[0] #'aabbccdd' -> '\xaa\xbb\xcc\xdd' -> int   '>L' means big-endian

        for i in range(0,len(data)/256+1):
            if i==len(data)/256 and i*256!=len(data):
                if(len(data)%4!=0):
                    for i in range(0,len(data)%4):
                        data=data+'\xff'
                self.BL.writeMemory(address+i*256 , data[i*256:])
            elif i*256!=len(data):
                self.BL.writeMemory(address+i*256 , data[i*256:i*256+256])
