import serial
from lib.DGCom import DGCom
#from PyQt5 import  QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class DGComQT():
    #@pyqtSlot(int)
    def init(self, initTrue):
        if initTrue:
            self.p400 = DGCom(port = 'COM9', timeout = 0.12)
            print('p400 connected', initTrue)
        else:
            self.p400.close()
            print('p400 disconnected', initTrue)
            
    def close(self):
        self.p400.close()
        
    def start(self, startStop):
        if startStop:
            self.p400.start()
            print('DG started')
        else:
            self.p400.stop()
            print('DG stoped')
            
    #@pyqtSlot(str)
    def setTrigSourse(self, sour = 'Ext'):
        self.p400.setTrigSourse(sour)
        
    #@pyqtSlot(str)
    def setTrigPol(self, pol = 'POS'):
        self.p400.setTrigPol(pol)
    
    #@pyqtSlot(str)
    def setTrigTerm(self, term = '50OHM'):
        self.p400.setTrigTerm(term)
        
    #@pyqtSlot(float)
    def setTrigV(self, volt = 0.6):
        self.p400.setTrigV(volt)
        
    #@pyqtSlot(int)
    def setTrigGM(self, mode = 1):
        self.p400.setTrigGM(mode)
                
    #for channels!!!!!!!!!!!!!!!!!!!
    #@pyqtSlot(tuple)
    def setChDelay(self, delay = 0, ch = 1): #1,0
        self.p400.setChDelay(ch, int(delay))
        
    #@pyqtSlot(tuple)
    def setChRelD(self, rel = 0, ch = 1):
        self.p400.setChRelD(ch, rel)
        
    #@pyqtSlot(str)
    def setChPol(self, pol = 'POS', ch = 'A'):
        if pol == 'POS':
            self.p400.setChPolPos(ch)
        else:
            self.p400.setChPolNeg(ch)
            
    #@pyqtSlot(tuple)
    def setChVHI(self, VHI = 2, ch ='A'):
        self.p400.setChVHI(ch, VHI)
        
    #@pyqtSlot(tuple)
    def setChVLO(self, VLO = 0, ch = 'A'):
        self.p400.setChVLO(ch, VLO)
        
    #@pyqtSlot(str)
    def chOnOff(self, onOff = 0, ch = 'A'):
        if onOff:
            self.p400.chOn(ch)
        else:
            self.p400.chOff(ch)


