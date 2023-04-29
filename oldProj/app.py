import thorlabs_apt as apt

import sys
import qdarkstyle
from PyQt5 import  QtGui, QtWidgets, QtCore
from mainwindow import Ui_MainWindow
from windowSpec import Ui_WindowSpec

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import cv2
import numpy as np
#from CameraClassWrapper import IDSCam
import csv
import os
import math 
from scipy.optimize import curve_fit
#import nicelib
#from instrumental import instrument, list_instruments
#from instrumental.drivers.cameras import uc480

import os, time
#from queue import Queue
from lib.camWork import camWork
from lib.HRICom import HRICom
from lib.DGComQT import DGComQT

#from pyueye import ueye
#from pyueye_example_utils import (MemoryInfo, uEyeException, Rect, get_bits_per_pixel,ImageBuffer, check)

from lib.mygraphicsview import MyGraphicsView
imageSizeUIx = 600
imageSizeUIy = 480


def readSpec(specName, delimiter):
    x = np.array([])
    y = np.array([])
    with open(specName, newline='') as f:
        fr = csv.reader(f, delimiter=delimiter, quotechar='|')
        for row in fr:
            if row != []:
                y = np.append(y, row[0])
                x = np.append(x, row[1])
                
    #x = x.astype(np.float)
    #y = y.astype(np.float)
    return y, x
tx, ty = readSpec('transmission_losgatos.dat', ' ')    

def func(x, a, b, c, d, e, f):
     return (a + b * x + c * x ** 2 + d * x ** 3 + e * x ** 4 + f * x ** 5)
     
def transM(y, x, ty, tx):
    
    xmin = min(np.where(tx >= min(x))[0])
    xmax = max(np.where(tx <= max(x))[0])
    xmax = max(np.where(tx <= max(x))[0])
    tx1 = tx[xmin:xmax]
    ty1 = ty[xmin:xmax]
    popt, pcov = curve_fit(func, tx1, 1/ty1)
    y1 = func(x,*popt)
    y1 = (y1 > 0) * y1
    y = y * y1
    y = y / y.max()
    
    return y,x
    
def checkName(file, add, folder = 'data'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    fileList = os.listdir(folder)
    fileGood = False
    ii = -1
    while fileGood is not True:
        ii += 1
        if file + str(ii) + add not in fileList:
            file = file + str(ii)
            fileGood = True
    file = folder + '//' + file + add
    return file
            
def writeSpec(folder, file, spec):
    file = checkName(file, '.csv', folder = 'data')
    
    with open(file, mode='w', newline='') as f:
        fw = csv.writer(f, delimiter = ',')
        for ii in range(spec[0].shape[0]):
            fw.writerow([spec[0][ii], spec[1][ii]])
            
def makeSpec(arr, topY, bottomY, pointR, pointG, waveR, waveG, backGround, backGroundUse, specLogUse):
    arr3 = np.copy(arr)
    backGround = np.copy(backGround)
    if len(arr3.shape) == 3:
        arr3 = cv2.cvtColor(arr3, cv2.COLOR_BGR2GRAY)
    
    #threshold = arr3.max()/5
    #arr3 = (arr3 > threshold) * arr3
    if pointR == pointG: 
        pointR = pointR + 1
    b = (waveR - waveG) / (pointR - pointG)
    a = waveR - b * pointR
    #topY = int(topY * arr3.shape[0]/imageSizeUIy)
    #bottomY = int(bottomY * arr3.shape[0]/imageSizeUIy)
    arr3[0:bottomY] = 0
    arr3[topY:] = 0
    pixSum = np.array([])
    pixSum = pixSum.astype(int)
    pixSum = np.sum(arr3, axis = 0)
    #print(max(pixSum))
    if backGroundUse and backGround.shape == arr3.shape:   
        #print(np.sum(backGround - backGround.astype(int)))
        #backGround = backGround.astype(int)
        backGround[0:bottomY] = 0
        backGround[topY:] = 0
        backSum = np.array([])
        backSum = np.sum(backGround, axis = 0)
        #print(max(backSum))
        diffSum = np.array([])
        diffSum = (pixSum > backSum) * (pixSum - backSum)
        #print(max(diffSum))
        #yAxes = (diffSum != 0) * (diffSum/ max(diffSum))
        yAxes = diffSum
    else:
        yAxes = pixSum
        #if max(pixSum != 0):
        #    yAxes = (pixSum != 0) * (pixSum/ max(pixSum))
        #else:
        #    yAxes = np.zeros(pixSum.shape)
        
    xAxes = np.linspace(a + b * 0, a + b * arr3.shape[1], arr3.shape[1])
    if specLogUse:
        yAxes, xAxes = transM(yAxes, xAxes, ty, tx)
    #if not (np.isnan(yAxes[0])) and yAxes[0] > 0:
        #yAxes, xAxes = transM(yAxes, xAxes)
    return yAxes, xAxes
#theory spectra
#constants and large omega
k = 1.3806504e-23
hb = 1.0545716e-34
h = (2.0*math.pi*1.0545716e-34) 
c = 2.9979246e+8
#mu
def defMu(u, numTotal, omega1, t):
    muD = -1e-18
    muT = -1e-36
    numLim = 2 * numTotal + 1
    while(abs(numLim - numTotal) > 1e-4):
        muM = -math.sqrt(muD * muT)
        numLim = distrib(t, muM, u, omega1).sum()
        if(numLim < numTotal):
            muD = muM
        else:
            muT = muM
    #print(muM)
    return muM
#energy distribution
def distrib(t, mu, u, omega1):
    n = np.array([])
    fg = np.vectorize(lambda x: 2 * float(x / (hb * omega1) + 1))
    g = fg(u)
    f = np.vectorize(lambda x: 1 /(np.exp(float(x - mu)/float(k*t)) - 1))
    num1 = f(u)
    num = g * num1
    return num
#get spec
def theorSpec(numTotal = 83000, modesNum = 1000,Lc = 585e-9,
            n = 1.4, q = 7 ,R = 1.0, t = 300):
    D0 = q * Lc / (n * 2) 
    omega1 = c / (n * math.sqrt(D0 * R / 2))
    #modes of oscilator
    u = np.arange(0, modesNum * hb * omega1, hb * omega1)
    E_tmp = u + h*c/Lc
    waveL = h*c/E_tmp
    mu = defMu(u, numTotal, omega1, t)
    num = distrib(t, mu, u, omega1)
    num = num/max(num)
    return num, waveL * 1e+9



def getCenter(image):
    image = np.copy(image)
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #threshold = image.max()/4
    #image = (image>=threshold)*image
    #moments = cv2.moments(image, 0) 
    #dM01 = moments['m01']                     # pixel sum in row
    #dM10 = moments['m10']                     # pixel sum in column
    #dArea = moments['m00']                     # pixel sum
    yAxes = np.sum(image, axis = 0) / ((max(np.sum(image, axis = 0))) + 1)
    #xAxes = np.linspace(a + b * 0, a + b * arr3.shape[1], arr3.shape[1])
    x = np.argmax(yAxes)
    y = 0
    #if dArea:
    #    x = int(dM10 / dArea)
    #    y = int(dM01 / dArea)       
    #else :
    #    y, x = image.shape
    #    y = y // 2
    #    x = x // 2
    return (int(x),int(y))
    
class Thread(QThread):
    #changePixmap = pyqtSignal(QImage)
    #changePixmap = pyqtSignal(np.ndarray)
    changePixmap = pyqtSignal(QPixmap)
    
    changePixmap2 = pyqtSignal(tuple)
    
    changePixTime = pyqtSignal(int)
    changeFps = pyqtSignal(float)
    changeExposure = pyqtSignal(float)
    changeBoost = pyqtSignal(int)
    
    getCenterL = pyqtSignal(int)
    getCenterR = pyqtSignal(int)
    save = False
    backTake = False
    backGroundUse = False
    gainBoost = False
    specLogUse = False
    backGround = np.array([])
    backGroundAvg = []
    arrAvL = []
    topY = 640
    bottomY = 0
    WVLeft = 0
    WVRight = 10
    pointWVLeft = 10
    pointWVRight = 580
    
    pixTime = 474
    fps = 3
    exposure = 200
    boost = 1450
    triggerDelay = 9960
    
    avgVid = 1
    findCenterLeft = False
    findCenterRight = False
    exposureMaxChecked = False
    iAv = 0
    iFAv = 0
    folder = str()
    #camCommandSignal = pyqtSignal([list])
    
    #|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #slots
    @pyqtSlot(int)
    def takeTopLevelS(self, topY):
        self.topY = topY
        
    @pyqtSlot(int)
    def takeBottomLevelS(self, bottomY):
        self.bottomY = bottomY
    
    @pyqtSlot(int)
    def takepointWVLeftS(self, pointWVLeft):
        self.pointWVLeft = pointWVLeft
    
    @pyqtSlot(int)
    def takepointWVRightS(self, pointWVRight):
        self.pointWVRight = pointWVRight

    @pyqtSlot(float)
    def takeWVLeftS(self, WVLeft):
        self.WVLeft = WVLeft

    @pyqtSlot(float)
    def takeWVRightS(self, WVRight):
        self.WVRight = WVRight
        
    @pyqtSlot()
    def takeCalimPointLeftS(self):
        self.findCenterLeft = True            
        
    @pyqtSlot()
    def takeCalimPointRightS(self):
        self.findCenterRight = True
        
    @pyqtSlot(float)
    def takeFpsS(self, fps):
        self.fps = fps
        self.cam.SetFramerate(self.fps)
    
    @pyqtSlot(float)
    def takeExposureS(self, exposure):
        self.exposure = exposure
        self.cam.SetExposure(self.exposure)
      
    @pyqtSlot(int)
    def pixTimeS(self, pixTime):
        self.pixTime = pixTime
        self.cam.SetPixelclock(self.pixTime)
        
    @pyqtSlot(int)
    def takeBoostS(self, boost):
        self.boost = boost
        self.cam.SetGain(self.boost)
       
    @pyqtSlot(int)
    def takeTriggerDelayS(self, triggerDelay):
        self.triggerDelay = triggerDelay
        self.cam.setTriggerDelay(self.triggerDelay)
        
    @pyqtSlot(int)
    def takeAvgVidS(self, avgVid):
        self.avgVid = avgVid
        
    @pyqtSlot(str)
    def saveS(self, folder = 'data'):
        self.save = True
        self.folder = folder
    @pyqtSlot()
    def backTakeS(self):
        self.backTake = True
        
    @pyqtSlot(bool)
    def backUseS(self, checked):
        self.backGroundUse = checked
    
    @pyqtSlot(bool)
    def gainBoostS(self, checked):
        self.cam.setGainBoost(checked)
        
        #self.gainBoost = checked
    
    @pyqtSlot(bool)
    def triggerS(self, checked):
        self.cam.setExternalTrigger(checked)
        self.cam.setTriggerDelay(self.triggerDelay)
        #self.gainBoost = checked
    
    @pyqtSlot(bool)
    def startStopS(self, checked):
        self.cam.freezeVIdeo(checked)
    
    @pyqtSlot(bool)
    def exposureMaxS(self, checked):
        self.exposureMaxChecked = checked
    
    @pyqtSlot(bool)
    def SpecLogS(self, checked):
        self.specLogUse = checked

    def run(self):
        cam = camWork(0)
        self.cam.SetPixelclock(self.pixTime)
        self.cam.SetFramerate(self.fps)
        self.cam.SetExposure(self.exposure)
        self.cam.SetGain(self.boost)

        #self.cam.GetExposure(),
        #self.cam.GetFramerate(),
        #print(self.cam.GetPixelclock())
        
        self.cam.captureVideo()
        
        iSum = 0
        arrSum = []
        
        colorTable = [QtGui.qRgb(i, 0, 0) for i in range(256)]
        _ = True
        while True:
            #if self.iFAv == 0:
                #time1 = time.time()
                
            if _: 
                frame_ = self.cam.takeImage().astype(dtype = 'uint8')
                _ = False

            frame = self.cam.takeImage().astype(dtype = 'uint8')
            #print(frame)
            if np.array_equal(frame, frame_) == False:
                
                self.iFAv = self.iFAv + 1
                self.arrAvL.append(np.copy(frame))
                _ = True
                
            #time.sleep(1)
            if self.iFAv >= self.avgVid and self.avgVid != 0:
                
                #print(time.time()-time1)
                #arr = np.zeros(frame.shape, dtype = 'uint8')
                arr = np.sum(self.arrAvL, axis = 0, dtype = 'uint8') #/ self.iFAv  #np.copy(frame)

                #arr = arr.astype(dtype = 'uint8')
                self.arrAvL = []
                self.iFAv = 0
                
                
                #here we compare real values and ui values
                
                if(self.pixTime != self.cam.GetPixelclock()):
                    self.pixTime = self.cam.GetPixelclock()
                    self.changePixTime.emit(self.pixTime)
                    
                if(self.boost != self.cam.GetGain()):
                    self.boost = self.cam.GetGain()
                    self.changeBoost.emit(self.boost)
                
                if(self.exposure != self.cam.GetExposure()):
                    self.exposure = self.cam.GetExposure()
                    self.changeExposure.emit(self.exposure)
                
                if(self.fps != self.cam.GetFramerate()):
                    self.fps = self.cam.GetFramerate()
                    self.changeFps.emit(self.fps)
                
                #max exposure
                if self.exposureMaxChecked:
                    if self.cam.getExposureMax != self.cam.GetExposure():
                        self.cam.setExposureMax()
                
                #take background
                if self.backTake:
                    self.backGroundAvg.append(arr)
                    self.iAv += 1
                    if self.iAv == 1:
                        self.backGroundAvg = np.array(self.backGroundAvg)
                        self.backGround = np.sum(self.backGroundAvg, axis = 0)/ self.iAv
                        self.backGround = self.backGround.astype(dtype = 'uint8') #dtype = 'uint')
                        self.backGroundAvg = []
                        self.iAv = 0
                        self.backTake = False
                
                #find left and right centers
                if self.findCenterLeft == True:
                    self.findCenterLeft = False
                    xCenterL, yCenterL = getCenter(arr)
                    self.getCenterL.emit(xCenterL)

                if self.findCenterRight == True:
                    self.findCenterRight = False
                    xCenterR, yCenterR = getCenter(arr)
                    self.getCenterR.emit(xCenterR)
                    
                # substract bg
                if self.backGround.shape == arr.shape and self.backGroundUse:
                    arr = (arr>self.backGround) * (arr - self.backGround)
                # check if the image colorful or bw. convert to qimage
                
                if len(arr.shape) == 3:
                    h, w, ch = arr.shape    
                    bytesPerLine = ch * w
                    convertToQtFormat = QtGui.QImage(arr.data, w, h, bytesPerLine, QtGui.QImage.Format_Grayscale8)
                else:
                    h, w = arr.shape
                    bytesPerLine = w

                    #convertToQtFormat = QtGui.QImage(arr.data, w, h, bytesPerLine, QtGui.QImage.Format_Indexed8)
                    convertToQtFormat = QtGui.QImage(arr.data, w, h, bytesPerLine, QtGui.QImage.Format_Grayscale8)
                    
                    
                #p = convertToQtFormat.scaled(imageSizeUIx, imageSizeUIy)#, Qt.KeepAspectRatio)
                p = convertToQtFormat.scaled(w, h, Qt.KeepAspectRatio)
                
                #print(p.height())
                #print(p.width())
                #p.setColorTable(colorTable)
                #p = p.convertToFormat(QImage.Format_RGB30)
                
                painter = QPainter()
                painter.begin(p)
                painter.setPen(QPen(Qt.blue, 2))
                topYUI = int(self.topY) # int(self.topY * imageSizeUIy / arr.shape[0])
                bottomYUI = int(self.bottomY) #int(self.bottomY * imageSizeUIy  / arr.shape[0])
                
                pointWVRightUI = int(self.pointWVRight)#int(self.pointWVRight * imageSizeUIx / arr.shape[1])
                pointWVLeftUI = int(self.pointWVLeft)#int(self.pointWVLeft * imageSizeUIx / arr.shape[1])
                
                #painter.drawLine(0, topYUI, imageSizeUIx, topYUI)
                #painter.drawLine(0, bottomYUI, imageSizeUIx, bottomYUI)
                painter.drawLine(0, topYUI, w, topYUI)
                painter.drawLine(0, bottomYUI, w, bottomYUI)
                
                painter.setPen(QPen(Qt.green, 2))
                #painter.drawLine(pointWVRightUI, 0, pointWVRightUI, imageSizeUIy)
                #painter.drawLine(pointWVLeftUI, 0, pointWVLeftUI, imageSizeUIy)
                painter.drawLine(pointWVRightUI, 0, pointWVRightUI, h)
                painter.drawLine(pointWVLeftUI, 0, pointWVLeftUI, h)
                
                painter.end()                                  
                #self.changePixmap.emit(p)
                #emit image
                #arr1 = np.copy(arr)
                #arr1[self.topY-2:self.topY+2, :] = 200
                #arr1[: ,self.pointWVRight-2:self.pointWVRight+2] = 100
                #arr1[: ,self.pointWVLeft-2:self.pointWVLeft+2] = 100
                #arr1[self.bottomY-5:self.bottomY+5, :] = 200
                pixMap = QPixmap.fromImage(p)
                self.changePixmap.emit(pixMap)
                
                #make spec
                #self.bottomY = self.topY - 1
                spectrum = makeSpec(arr, self.topY, #self.bottomY
                self.topY - 1, self.pointWVRight, self.pointWVLeft, self.WVRight, self.WVLeft, self.backGround, self.backGroundUse, self.specLogUse)
                
                #emit spec
                theorSpectrum = theorSpec()
                self.changePixmap2.emit((spectrum, theorSpectrum))
                #self.changePixmap2.emit(theorSpectrum)
                
                #save image and spec
                if self.save:
                    self.save = False
                    fileIm = checkName('img', '.png', self.folder)
                    cv2.imwrite(fileIm, arr)
                    writeSpec(self.folder, 'spec', spectrum)
                    
"""
class ThreadStage(QThread):
    #signals
    print('hui')
    stagePosS = pyqtSignal(str)
    
    #self.stagePos = 0.0
    devList = apt.list_available_devices()
    print('available devices from thorlabs', devList, 'stage info',apt.hardware_info(devList[0][1]))
    dev1 = devList[0][1]
    motor = apt.Motor(dev1)
    #motor.serial_number
    #motor.is_in_motion
    velParLimt = motor.get_velocity_parameter_limits()
    print('velocity limits', velParLimt)
    velPar = motor.get_velocity_parameters() #min vel, acc, max vel
    print('min vel, acc, max vel',velPar)
    
    motor.set_velocity_parameters(velPar[0], velPar[1], velPar[2])
    
    velPar = motor.get_velocity_parameters() #min vel, acc, max vel
    print('min vel, acc, max vel',velPar)
    #motor.get_velocity_parameter_limits() #max acc, max vel
    #motor.get_move_home_parameters() #(direction, limiting switch, velocity, zero offset)
    #motor.get_stage_axis_info()
    #motor.is_in_motion()
    stageSetPosBool = False
    stageHomeBool = False
    setPos = 0
    velocity = float()
    
    #print(motor.is_in_motion, type(motor.is_in_motion))
    
    @pyqtSlot(float)
    def stageSetPosS(self, setPos):
        self.stageSetPosBool = True
        self.setPos = setPos
        self.start()
        
    def stageHome(self):
        self.stageHomeBool = True
        self.start()
        
    pyqtSlot(float)
    def stageSetVelocityS(self, velocity):
        #self.velocity = velocity
        velPar = self.motor.get_velocity_parameters()
        self.motor.set_velocity_parameters(velPar[0], velPar[1], velocity)
        velPar = self.motor.get_velocity_parameters()
        print('velocity parameters', velPar)
        
    def closeEvent():
        pass
        #apt._cleanup()
        #print('stage class closed')
        
    def run(self):
        self.stagePosS.emit(str(self.motor.position))
        
        ii = 0
        print('stage started to move')
        while self.motor.is_in_motion or ii == 0:
            ii += 1
                
            if self.stageSetPosBool:
                self.stageSetPosBool = False
                #self.stagePosS.emit(str(self.motor.position))
                self.motor.move_to(self.setPos)
                #time.sleep(1)
                #self.stagePosS.emit(str(self.motor.position))
            if self.stageHomeBool:
                self.stageHomeBool = False
                #self.stagePosS.emit(str(self.motor.position))
                self.motor.set_move_home_parameters(2, 1, 2.2,0)
                self.motor.move_home()
                #time.sleep(2)
                #self.stagePosS.emit(str(self.motor.position))
            time.sleep(0.05)
            self.stagePosS.emit(str(self.motor.position))
            #self.stagePosS.emit(str(self.motor.position))
        #    self.stagePosS.emit(str(self.motor.position))
            #motor.move_to(3)
        print('the stage stoped movement')
"""        
        
def checkFolderExp(direct = 'data/exp'):
    ii = 0
    folder = '666'
    while ii < 6666:
        ii += 1
        folder = direct + str(ii)
        if not os.path.exists(folder):
            ii = 6668
    return(folder)
    
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
        
def main():
    app = QtWidgets.QApplication(sys.argv )
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    windowSpec = QWidget()
    ui2 = Ui_WindowSpec()
    ui2.setupUi(windowSpec)
    #windowSpec.show()
    
    app.aboutToQuit.connect(ui.closeEvent)
    #app.aboutToQuit.connect(ThreadStage.closeEvent)
    
    th = Thread()
    th.changePixmap.connect(ui.setImage)
    th.changePixmap2.connect(ui.setSpectrum)
    
    ui.takeTopLevel.connect(th.takeTopLevelS)
    ui.takeBottomLevel.connect(th.takeBottomLevelS)
    ui.takeWVLeft.connect(th.takeWVLeftS)
    ui.takeWVRight.connect(th.takeWVRightS)
    ui.takePointWVLeft.connect(th.takepointWVLeftS)
    ui.takePointWVRight.connect(th.takepointWVRightS)
    ui.takeCalimPointLeft.connect(th.takeCalimPointLeftS)
    ui.takeCalimPointRight.connect(th.takeCalimPointRightS)
    ui.takeFps.connect(th.takeFpsS)
    ui.takeExposure.connect(th.takeExposureS)
    ui.takeBoost.connect(th.takeBoostS)
    ui.takeTriggerDelay.connect(th.takeTriggerDelayS)
    ui.takeAvgVid.connect(th.takeAvgVidS)
    
    ui.saveSi.connect(th.saveS)
    
    ui.pushButtonBackTake.clicked.connect(th.backTakeS)
    ui.backUse.connect(th.backUseS)
    ui.gainBoost.connect(th.gainBoostS)
    ui.trigger.connect(th.triggerS)
    ui.startStop.connect(th.startStopS)
    ui.exposureMax.connect(th.exposureMaxS)
    ui.takePixTime.connect(th.pixTimeS)
    ui.SpecLog.connect(th.SpecLogS)
    ui.pushButtonBackTake.clicked.connect(th.backTakeS)
    
    ui.checkBoxInitCam.stateChanged.connect(th.start)
    
    th.changeFps.connect(ui.spinBoxFps.setValue)
    th.changeExposure.connect(ui.spinBoxExposure.setValue)
    th.changeBoost.connect(ui.spinBoxBoost.setValue)
    th.changePixTime.connect(ui.spinBoxPixTime.setValue)
    
    th.getCenterL.connect(ui.spinBoxPointWLLeft.setValue)
    th.getCenterR.connect(ui.spinBoxPointWLRight.setValue)
    #th..connect(ui.checkBoxGainBoost.isChecked)
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #stage
    
    """ 
    thStage = ThreadStage()
    thStage.stagePosS.connect(ui.labelPositionShow.setText)
    ui.stageSetPosE.connect(thStage.stageSetPosS)
    ui.takeStageVelocity.connect(thStage.stageSetVelocityS)
    ui.pushButtonStageHome.clicked.connect(thStage.stageHome)
    
    thStage.stagePosS.emit(str(thStage.motor.position))
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    thExp = ThreadExp()
    ui.expStartSi.connect(thExp.expStartS)
    ui.expStartSi.connect(thExp.start)
    thExp.stageSetPosSi.connect(thStage.stageSetPosS)
    thExp.saveSi.connect(th.saveS)
    
    
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #thwind = addWind()
    #th.changePixmap.connect(thwind.setImage)
    #thwind.start()
    
    th.start()
    """
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #HRI
    thHri = HRI()
    ui.HRIInit.connect(thHri.init)
    
    ui.pushButtonRemote.clicked.connect(thHri.remMode)
    ui.pushButtonLocal.clicked.connect(thHri.locMode)
    ui.pushButton50Trig.clicked.connect(thHri.set50Trig)
    ui.pushButtonHiTrig.clicked.connect(thHri.setHiTrig)
    ui.pushButtonPosTrig.clicked.connect(thHri.setPosTrig)
    ui.pushButtonNegTrig.clicked.connect(thHri.setNegTrig)
    ui.pushButtonStat.clicked.connect(thHri.stat)
    ui.pushButtonRev.clicked.connect(thHri.rev)
    ui.takeMCP.connect(thHri.setMCP)
    ui.takeHRIThr.connect(thHri.setHRIThr)
    ui.comboBoxMode.currentTextChanged.connect(thHri.setMode)
    
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #P400
    thP400 = DGComQT()
    #triger
    ui.checkBoxDGInit.stateChanged.connect(thP400.init)
    ui.checkBoxDGStart.stateChanged.connect(thP400.start)
    ui.comboBoxDGSource.currentTextChanged.connect(thP400.setTrigSourse)
    ui.comboBoxDGEdge.currentTextChanged.connect(thP400.setTrigPol)
    ui.comboBoxDGTerm.currentTextChanged.connect(thP400.setTrigTerm)
    ui.comboBoxDGGateMode.currentTextChanged.connect(thP400.setTrigGM)
    ui.doubleSpinBoxDGLvl.valueChanged.connect(thP400.setTrigV)
    #channel A
    ui.doubleSpinBoxDGAdelay.valueChanged.connect(thP400.setChDelay)
    ui.doubleSpinBoxDGAVHigh.valueChanged.connect(thP400.setChVHI)
    ui.doubleSpinBoxDGAVLow.valueChanged.connect(thP400.setChVLO)
    ui.comboBoxDGARefCh.currentTextChanged.connect(thP400.setChRelD)
    ui.comboBoxDGAPol.currentTextChanged.connect(thP400.setChPol)
    ui.checkBoxDGAOn.stateChanged.connect(thP400.chOnOff)
    
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #thStage.start()
    #thExp.start()
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    ui.spinBoxTop.setValue(1190)
    ui.spinBoxBottom.setValue(1800)
    ui.doubleSpinBoxWLLeft.setValue(590.49 )
    ui.doubleSpinBoxWLRight.setValue(584.00)
    ui.spinBoxPointWLRight.setValue(0)
    ui.spinBoxPointWLLeft.setValue(236)
 
    sys.exit( app.exec_() )
    
if __name__ == "__main__":
    main()