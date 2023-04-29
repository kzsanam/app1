import sys
import qdarkstyle
from PyQt5 import  QtGui, QtWidgets, QtCore
from mainwindow import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
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
#from camWorkThor import camWork
#from pyueye import ueye
#from pyueye_example_utils import (MemoryInfo, uEyeException, Rect, get_bits_per_pixel,ImageBuffer, check)

import lib.appFunc as mf
from lib.appFunc import makeSpec, checkName, theorSpec, writeSpec, getCenter, specFit, convolution

imageSizeUIx = 600
imageSizeUIy = 480

class ThreadSpec(QThread):
    changePixmap = pyqtSignal(QImage)
    changePixmap2 = pyqtSignal(tuple)
    
    changeFps = pyqtSignal(float)
    changeExposure = pyqtSignal(float)
    changeBoost = pyqtSignal(int)
    
    getCenterL = pyqtSignal(int)
    getCenterR = pyqtSignal(int)
    findPhNum = pyqtSignal(str)
    
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
    fps = 3
    exposure = 300
    boost = 2000
    triggerDelay = 9960
    avgVid = 1
    findCenterLeft = False
    findCenterRight = False
    exposureMaxChecked = False
    iAv = 0
    iFAv = 0
    #camCommandSignal = pyqtSignal([list])
    
    
    @pyqtSlot(int)
    def initCam(self, initCam):
            self.initCam = initCam
            
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
        
    @pyqtSlot()
    def saveS(self):
        self.save = True

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
        print('spec is started')
        self.cam = camWork(12)
        print('pix clock', self.cam.GetPixelclock())
        self.cam.SetPixelclock(35)
        print('pix clock', self.cam.GetPixelclock())
        self.cam.captureVideo()        
        self.cam.SetFramerate(self.fps)
        self.cam.SetExposure(self.exposure)
        self.cam.SetGain(self.boost)

        #self.cam.GetExposure(),
        #self.cam.GetFramerate(),

        
        iSum = 0
        arrSum = []
        saveCount = 0
        waitcount = 0
        while 1 == 1:  
            
            frame = self.cam.takeImage()
            self.iFAv = self.iFAv + 1
            self.arrAvL.append(np.copy(frame))
            
            if self.iFAv == self.avgVid:
                arr = np.sum(self.arrAvL, axis = 0) / self.iFAv  #np.copy(frame)
                arr = arr.astype(dtype = 'uint8')
                self.arrAvL = []
                self.iFAv = 0
                
                
                #here we compare real values and ui values
                if(self.boost != self.cam.GetGain()):
                    self.boost = self.cam.GetGain()
                    self.changeBoost.emit(self.boost)
                
                if(self.exposure != self.cam.GetExposure()):
                    self.exposure = self.cam.GetExposure()
                    self.changeExposure.emit(self.exposure)
                
                if(self.fps != self.cam.GetFramerate()):
                    self.fps = self.cam.GetFramerate()
                    self.changeFps.emit(self.fps)
                
                if self.exposureMaxChecked:
                    if self.cam.getExposureMax != self.cam.GetExposure():
                        self.cam.setExposureMax()
                
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
                        
                spectrum = makeSpec(arr, self.topY, self.bottomY, self.pointWVRight, self.pointWVLeft, self.WVRight, self.WVLeft, self.backGround, self.backGroundUse, self.specLogUse)
                
                #arr[0:self.topY] = 0
                #arr[self.bottomY:] = 0
                #arr[0:self.bottomY] = 0
                #arr[self.topY:] = 0
                if self.findCenterLeft == True:
                    self.findCenterLeft = False
                    xCenterL, yCenterL = getCenter(arr)
                    self.getCenterL.emit(xCenterL)

                if self.findCenterRight == True:
                    self.findCenterRight = False
                    xCenterR, yCenterR = getCenter(arr)
                    self.getCenterR.emit(xCenterR)
                    
                if self.backGround.shape == arr.shape and self.backGroundUse:
                    arr = (arr>self.backGround) * (arr - self.backGround)
                    
                if len(arr.shape) == 3:
                    h, w, ch = arr.shape    
                    bytesPerLine = ch * w
                    convertToQtFormat = QtGui.QImage(arr.data, w, h, bytesPerLine, QtGui.QImage.Format_Grayscale8)
                else:
                    h, w = arr.shape
                    bytesPerLine = w
                    
                    convertToQtFormat = QtGui.QImage(arr.data, w, h, bytesPerLine, QtGui.QImage.Format_Grayscale8)
                p = convertToQtFormat.scaled(imageSizeUIx, imageSizeUIy)#, Qt.KeepAspectRatio)
                #print(p.height())
                #print(p.width())
                painter = QPainter()
                painter.begin(p)
                painter.setPen(QPen(Qt.blue, 3))
                topYUI = int(self.topY * imageSizeUIy / arr.shape[0])
                bottomYUI = int(self.bottomY * imageSizeUIy  / arr.shape[0])
                #print(self.bottomY)
                #print(topYUI)
                pointWVRightUI = int(self.pointWVRight * imageSizeUIx / arr.shape[1])
                pointWVLeftUI = int(self.pointWVLeft * imageSizeUIx / arr.shape[1])
                painter.drawLine(0, topYUI, imageSizeUIx, topYUI)
                painter.drawLine(0, bottomYUI, imageSizeUIx, bottomYUI)
                painter.setPen(QPen(Qt.green, 3))
                painter.drawLine(pointWVRightUI, 0, pointWVRightUI, imageSizeUIy)
                painter.drawLine(pointWVLeftUI, 0, pointWVLeftUI, imageSizeUIy)
                
                painter.end()                                  
                self.changePixmap.emit(p)
                #phNum = round(specFit(spectrum[1], spectrum[0]),1)
                #self.findPhNum.emit(str(phNum))
                Lc = spectrum[1][np.argmax(spectrum[0])] * 1e-9
                #theorSpectrum = theorSpec(numTotal = phNum, modesNum = 1000,Lc = Lc, n = 1.4, q = 7 ,R = 1.0, t = 300)
                #theorSpectrum = convolution(theorSpectrum[0], theorSpectrum[1], 90)
                theorSpectrum = np.copy(spectrum)
                self.changePixmap2.emit((spectrum, theorSpectrum))
                #self.changePixmap2.emit(theorSpectrum)
                
                #print(findPhNum)
                if self.save:
                    #self.save = False
                    waitcount += 1
                    if saveCount > 20:
                        self.save = False
                        saveCount = 0
                        
                    if waitcount > 10:
                        waitcount = 0
                        saveCount += 1
                        fileIm = checkName('img', '.png')
                        cv2.imwrite(fileIm, arr)
                        writeSpec('data', 'spec', spectrum)
