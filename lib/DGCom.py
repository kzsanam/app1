import serial

class DGCom():
    def __init__(self, port = 'COM9', baudrate = 38400, 
                 timeout = 0.12, bytesize = 8, parity = 'N', stopbits=1):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout
        self.ser.bytesize = bytesize
        self.ser.parity = parity
        self.ser.stopbits = stopbits
        self.ser.open()
        
    def writeRead(self, a):
        self.ser.write(a)
        print(self.ser.readline())
    
    def start(self):
        self.writeRead(b'STA\r\n')
    
    def stop(self):
        self.writeRead(b'STO\r\n')
    
    def setTrigSourse(self, sour = 'EXT'):
        self.writeRead(b'TRIG:SOUR ' + bytes(str(sour), 'ascii') + b'\r\n')
        self.writeRead(b'TRIG:SOUR?\r\n')
        
    def setTrigPol(self, pol = 'POS'):
        self.writeRead(b'TRIG:INPUT:POL ' + bytes(str(pol), 'ascii') + b'\r\n')
        self.writeRead(b'TRIG:INPUT:POL?\r\n')
    
    def setTrigTerm(self, term = '50OHM'):
        #HIGHZ - HIGH
        self.writeRead(b'TRIG:INPUT:TERM ' +  bytes(str(term), 'ascii') + b'\r\n')
        self.writeRead(b'TRIG:INPUT:TERM?\r\n')
        
    def setTrigV(self, volt):
        self.writeRead(b'TRIG:INPUT:VOLT ' + bytes(str(volt), 'ascii') + b'\r\n')
        self.writeRead(b'TRIG:INPUT:VOLT?\r\n')
        
    def setTrigGM(self, mode = 1):
        self.writeRead(b'GATE:MOD ' + bytes(str(mode), 'ascii') + b'\r\n')
        self.writeRead(b'GATE:MOD?\r\n')
                
    def setChDelay(self, ch = 1, delay = 0):
        #1 - a leading
        self.writeRead(b'TIME:DEL' + bytes(str(ch), 'ascii') + b' ' + bytes(str(delay), 'ascii') + b'PS\r\n')
        self.writeRead(b'TIME:DEL' + bytes(str(ch), 'ascii') + b'?\r\n')
        
    def setChRelD(self, ch = 1, chrel = 0):
        #1 - a leading, 0 - to
        self.writeRead(b'TIME:RELT' + bytes(str(ch), 'ascii') + b' ' + bytes(str(chrel), 'ascii') + b'\r\n')
        self.writeRead(b'TIME:RELT' + bytes(str(ch), 'ascii') + b'?\r\n')

    def setChPolPos(self, ch = 'A'):
        self.writeRead(b'CHAN:'+ bytes(str('POS'), 'ascii') + b' ' + bytes(str(ch), 'ascii') + b'\r\n')
        self.writeRead(b'CHAN:POS? ' + bytes(str(ch), 'ascii') + b'\r\n')
        
    def setChPolNeg(self, ch = 'A'):
        self.writeRead(b'CHAN:'+ bytes(str('NEG'), 'ascii') + b' ' + bytes(str(ch), 'ascii') + b'\r\n')
        self.writeRead(b'CHAN:NEG? ' + bytes(str(ch), 'ascii') + b'\r\n')

    def setChVHI(self, ch = 'A', VHI = 2):
        self.writeRead(b'CHAN:VHI '+ bytes(str(ch), 'ascii') + b', ' + bytes(str(VHI), 'ascii') + b'\r\n')
        self.writeRead(b'CHAN:VHI? ' + bytes(str(ch), 'ascii') + b'\r\n')

    def setChVLO(self, ch = 'A', VLO = 0):
        self.writeRead(b'CHAN:VLO '+ bytes(str(ch), 'ascii') + b', ' + bytes(str(VLO), 'ascii') + b'\r\n')
        self.writeRead(b'CHAN:VLO? ' + bytes(str(ch), 'ascii') + b'\r\n')

    def chOff(self, ch = 'A'):
        self.writeRead(b'CHAN:OFF ' + bytes(str(ch), 'ascii') + b'\r\n')
        self.writeRead(b'CHAN:OFF? ' + bytes(str(ch), 'ascii') + b'\r\n')

    def chOn(self, ch = 'A'):
        self.writeRead(b'CHAN:ON ' + bytes(str(ch), 'ascii') + b'\r\n')
        self.writeRead(b'CHAN:ON? ' + bytes(str(ch), 'ascii') + b'\r\n')

    def close(self):
        self.ser.close()
