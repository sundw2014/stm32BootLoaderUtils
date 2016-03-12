# -*- coding:utf-8 -*-

'provide some basic operation including read, write, erase ...'
__author__ = 'sundw2014'

import serial,struct

timeout=1;
buadRate=9600;

class BootLoader(object):
    def __init__(self,serPath):
        self.ser = serial.Serial(serPath, buadRate, timeout=timeout, parity=serial.PARITY_EVEN)
        if(not self.ser.isOpen()):
            print('open %s failed\r\n' % serPath)
        self.ready=False

    def begin(self):
        self.ser.write('\x7F')
        response=self.ser.read(1)
        if(response[0]=='\x79'):
            self.ready=True
            return True
        else:
            print('start failed\r\n')
            self.ready=False
            return False

    def getCommand(self):
        pass

    def getVersionAndProtectionStatus(self):
        pass

    def getID(self):
        pass

    def writeMemory(self , address , data):
        if(not self.ready):
            print("target not ready\r\n")
            return False

        self.ser.write('\x31\xCE')#command magic number and its complement
        if(self.ser.read(1)[0]!='\x79'):
            print('NO CORRECT ACK! internal error\r\n')
            return False
        hexAddress=hex(address)[2:]
        if len(hexAddress)%2:
            hexAddress='0'+hexAddress
        self.ser.write(hexAddress.decode('hex'))

        B1,B2,B3,B4=struct.unpack('4B' , hexAddress.decode('hex'))
        self.ser.write(struct.pack('B',B1^B2^B3^B4))
        if(self.ser.read(1)[0]!='\x79'):
            print('NO CORRECT ACK! internal error\r\n')
            return False
        print(len(data))
        print('\n')
        self.ser.write(struct.pack('B' , len(data)-1))
        self.ser.write(data)

        XOR=len(data)-1
        for b in data:
            XOR=XOR^struct.unpack('B' , b)[0]
        self.ser.write(struct.pack('B' , XOR))
        if(self.ser.read(1)[0]!='\x79'):
            print('NO CORRECT ACK! internal error\r\n')
            return False
        return True

    def readMemory(self):
        pass

    def eraseMemory(self):
        pass

    def eraseAllMemory(self):
        #if(not self.ready):
        #    print("target not ready\r\n")
        #    return False

        self.ser.write('\x43\xBC')#command magic number and its complement
        if(self.ser.read(1)[0]!='\x79'):
            print('NO CORRECT ACK! internal error\r\n')
            return False
        self.ser.write('\xFF\x00')
        if(self.ser.read(1)[0]!='\x79'):
            print('eraseAllMemory operation failed! internal error\r\n')
            return False
        return True

    def writeUnprotection(self):
        if(not self.ready):
            print("target not ready\r\n")
            return False

        self.ser.write('\x73\x8C')#command magic number and its complement
        if(self.ser.read(1)[0]!='\x79'):
            print('NO CORRECT ACK! internal error\r\n')
            return False
        if(self.ser.read(1)[0]!='\x79'):
            print('write unprotect operation failed! internal error\r\n')
            return False

    def readUnprotection(self):
        if(not self.ready):
            print("target not ready\r\n")
            return False

        self.ser.write('\x92\x6D')#command magic number and its complement
        if(self.ser.read(1)[0]!='\x79'):
            print('NO CORRECT ACK! internal error\r\n')
            return False
        if(self.ser.read(1)[0]!='\x79'):
            print('read unprotect operation failed! internal error\r\n')
            return False
