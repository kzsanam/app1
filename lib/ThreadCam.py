import sys

from PyQt5 import  QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from mainwindow import Ui_MainWindow
from windowSpec import Ui_WindowSpec

import cv2
import numpy as np
import csv
import os
import math 
from scipy.optimize import curve_fit
import os, time

from lib.camWorkPylon import camWork
from lib.appFunc import makeSpec, checkName, theorSpec, writeSpec, getCenter, calcArrScan, checkFolderExp

imageSizeUIx = 600
imageSizeUIy = 480

class ThreadCam(QThread):
    changePixmap = pyqtSignal(QPixmap)
    changePixmap2 = pyqtSignal(tuple)
    changeScanPlot = pyqtSignal(np.ndarray)
    
    changePixTime = pyqtSignal(int)
    changeFps = pyqtSignal(float)
    changeExposure = pyqtSignal(float)
    changeBoost = pyqtSignal(int)
    
    getCenterL = pyqtSignal(int)
    getCenterR = pyqtSignal(int)
    changeScanPos = pyqtSignal(int)
    
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
    
    pixTime = 0
    fps = 50
    exposure = 200000
    boost = 0
    triggerDelay = 9960
    
    avgVid = 1
    findCenterLeft = False
    findCenterRight = False
    exposureMaxChecked = False
    iAv = 0
    iFAv = 0
    folder = str()
    #|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #slots
    @pyqtSlot(int)
    def takeTopLevelS(self, topY):
        self.topY = topY
        
    @pyqtSlot(int)
    def takeBottomLevelS(self, bottomY):
        self.bottomY = bottomY
        
    def boxLeftSl(self, boxLeft):
        self.boxLeft = boxLeft

    def boxRightSl(self, boxRight):
        self.boxRight = boxRight
    
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
    
    @pyqtSlot(bool)
    def triggerS(self, checked):
        self.cam.setExternalTrigger(checked)
        self.cam.setTriggerDelay(self.triggerDelay)
    
    @pyqtSlot(bool)
    def startStopS(self, checked):
        self.cam.freezeVIdeo(checked)
    
    @pyqtSlot(bool)
    def exposureMaxS(self, checked):
        self.exposureMaxChecked = checked
        
    @pyqtSlot(bool)
    def SpecLogS(self, checked):
        self.specLogUse = checked

    def initCam(self, initCam):
            self.initCam = initCam
            
    def changeImQual(self, changeImQual):
        self.changeImQual = changeImQual

    def ScanOnPlaceStart(self):
        if self.ScanStart == True:
            self.ScanStart = False
        self.arrScan = np.array([])
        self.ScanOnPlaceStart = not self.ScanOnPlaceStart
    
    def ScanStartSl(self):
        if self.ScanOnPlaceStart == True:
            self.ScanOnPlaceStart = False
        self.arrScan = np.array([])
        self.ScanStart = not self.ScanStart
        
    def scanSave(self):
        np.savetxt("data/scan.csv", self.arrScan, delimiter=",")
        
    def run(self):
        self.cam = camWork(0)
        self.cam.SetPixelclock(self.pixTime)
        self.cam.SetFramerate(self.fps)
        self.cam.SetExposure(self.exposure)
        self.cam.SetGain(self.boost)
        self.changeImQual = 0
        self.ScanOnPlaceStart = False
        self.ScanStart = False
        self.arrScan = np.array([])
        iscan = 0
        #self.cam.GetExposure(),
        #self.cam.GetFramerate(),
        #print(self.cam.GetPixelclock())
        
        self.cam.captureVideo()
        iSum = 0
        arrSum = []
        
        colorTable = [QtGui.qRgb(i, 0, 0) for i in range(256)]
        _ = True
        while self.initCam != 0:
            #if self.iFAv == 0:
                #time1 = time.time()
                
            #if _: 
            #    frame_ = self.cam.takeImage().astype(dtype = 'uint8')
            #    _ = False

            frame = self.cam.takeImage().astype(dtype = 'uint8')
            frame = frame[:,:,0]
            frame = np.rot90(frame)
            #print(frame)
            #if np.array_equal(frame, frame_) == False:
            if 1==1:
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
                #scan
                if self.ScanOnPlaceStart:
                    self.arrScan = calcArrScan(self.arrScan, 
                    arr[self.topY:self.bottomY, self.boxLeft:self.boxRight])
                    self.changeScanPlot.emit(self.arrScan)
                    
                if self.ScanStart:
                    #need to add here start stop and step
                    #f iscan*scanStep < scanEnd:
                    #    self.changeScanPos(begin + i*step)
                    #else iscan = 0
                    
                    self.arrScan = calcArrScan(self.arrScan, 
                    arr[self.topY:self.bottomY, self.boxLeft:self.boxRight])
                    self.changeScanPlot.emit(self.arrScan)
                    

                # check if the image colorful or bw. convert to qimage
                
                if len(arr.shape) == 3:
                    #print('hui3')
                    h, w, ch = arr.shape    
                    bytesPerLine = ch * w
                    convertToQtFormat = QtGui.QImage(arr.data, w, h, bytesPerLine, QtGui.QImage.Format_Grayscale8)
                else:
                    #print('hui')
                    h, w = arr.shape
                    bytesPerLine = w

                    #convertToQtFormat = QtGui.QImage(arr.data, w, h, bytesPerLine, QtGui.QImage.Format_Indexed8)
                    convertToQtFormat = QtGui.QImage(arr.data, w, h, bytesPerLine, QtGui.QImage.Format_Grayscale8)
                    
                if self.changeImQual:
                    p = convertToQtFormat.scaled(w, h, Qt.KeepAspectRatio)
                else:
                    p = convertToQtFormat.scaled(imageSizeUIx, imageSizeUIy, Qt.KeepAspectRatio)
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
                
                painter.drawLine(self.boxRight, 0, self.boxRight, h)
                painter.drawLine(self.boxLeft, 0, self.boxLeft, h)
                
                #painter.drawLine(pointWVRightUI, 0, pointWVRightUI, h)
                #painter.drawLine(pointWVLeftUI, 0, pointWVLeftUI, h)
                
                painter.end()                                  
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
        else:
            self.cam.Exit()