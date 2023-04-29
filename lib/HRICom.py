import serial

modesWords = [
    "Inhibit",
"<50ps comb",
"50ps comb",
"100ps comb",
"150ps comb",
"200ps comb",
"1000ps comb",
"2000ps comb",
"3000ps comb",
"4000ps comb",
"5000ps comb",
"DC"
]

modesNums = [
    0,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    24
]
modes = [modesNums, modesWords]


class HRICom():

    def __init__(self, port = 'COM8', baudrate = 115200, 
                 timeout = 0.12, bytesize = 8, parity = 'N', stopbits=1):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout
        self.ser.bytesize = bytesize
        self.ser.parity = parity
        self.ser.stopbits = stopbits
        self.ser.open()
        
    def readResp(self):
        st = self.ser.readline()
        print(st)
        while not (b'ok' in st) and st != b'':
            st = self.ser.readline()
            print(st)
            
    def rev(self):
        self.ser.write(b'.REV\r\n')
        self.readResp()
        
    def remMode(self):
        self.ser.write(b'\r\n')
        self.readResp()
        
    def locMode(self):
        self.ser.write(b'\r\n')
        self.readResp()
        
    def stat(self):
        self.ser.write(b'.STATUS\r\n')
        self.readResp()
        
    def setMode(self, mode):
        self.ser.write(bytes(str(mode), 'ascii') + b' !MODE\r\n')
        self.readResp()
        
    def setModeWord(self, mode):
        mode = modes[0][modes[1].index(mode)]
        self.ser.write(bytes(str(mode), 'ascii') + b' !MODE\r\n')
        self.readResp()
        
    def setMCP(self,mcp):
        self.ser.write(bytes(str(mcp), 'ascii')+b' !MCP\r\n')
        self.readResp()
        
    def setThr(self, thr):
        self.ser.write(bytes(str(thr), 'ascii')+b' !THRESH\r\n')
        self.readResp()    
     
    def set50Trig(self):
        self.ser.write(b'50TRIG\r\n')
        self.readResp()
        
    def setHiTrig(self):
        self.ser.write(b'HITRIG\r\n')
        self.readResp()
        
    def setPosTrig(self):
        self.ser.write(b'+VETRIG\r\n')
        self.readResp()
        
    def setNegTrig(self):
        self.ser.write(b'-VETRIG\r\n')
        self.readResp()        
        
    def close(self):
        self.ser.close()