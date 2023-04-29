from PyQt5.QtCore import *
import time 
import numpy as np
from lib.appFunc import checkFolderExp

class ThreadExp(QThread):
    stageSetPosSi = pyqtSignal(float)
    saveSi = pyqtSignal(str)
    
    expStartB = False
    expStep = 0.00005
    expStartPos = float()
    expStopPos = float()
    folder = ''
    avgN = 1
        
    @pyqtSlot(tuple)
    def expStartS(self, startStopPos):
        self.expStartB = True
        expStartPos, expStopPos = startStopPos
        self.expStartPos = expStartPos
        self.expStopPos = expStopPos
        
    def run(self):
        self.folder = checkFolderExp()
        while self.expStartB:
            if self.expStartB:
                self.expStartB = False
                start_time = time.time()
                for pos in np.arange(self.expStartPos, self.expStopPos + self.expStep, self.expStep):
                    self.stageSetPosSi.emit(pos)
                    print(pos)
                    time.sleep(3)
                    for _ in range(self.avgN):
                        self.saveSi.emit(self.folder)
                print('time of work', time.time() - start_time)
                print('finished', 'avg =', self.avgN)
                #save parameters. start, end, step, avg
           