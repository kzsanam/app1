from lib.HRICom import HRICom

from PyQt5.QtCore import *

class HRI(QThread):
    @pyqtSlot(bool)
    def init(self, initTrue):
        if initTrue:
            self.hri = HRICom(port = 'COM8', timeout = 0.12)
            self.hri.set50Trig()
        else:
            self.hri.setModeWord('Inhibit')
            self.hri.close()
            
    def remMode(self):
        self.hri.remMode() 
        
    def locMode(self):
        self.hri.locMode()
        
    def set50Trig(self):
        self.hri.set50Trig()
            
    def setHiTrig(self):
        self.hri.setHiTrig()
    
    def setPosTrig(self):
        self.hri.setPosTrig()
    
    def setNegTrig(self):
        self.hri.setNegTrig()
    
    def stat(self):
        self.hri.stat()

    def rev(self):
        self.hri.rev()

    @pyqtSlot(int)
    def setMCP(self, MCP):
        self.hri.setMCP(MCP)
        
    @pyqtSlot(int)
    def setHRIThr(self, thr):
        self.hri.setThr(thr)

    @pyqtSlot(str)
    def setMode(self, mode):
        self.hri.setModeWord(mode)
     