from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
from lib.mygraphicsview import MyGraphicsView
import time
imageSizeUIx = 600
imageSizeUIy = 480

def restore(settings):
    finfo = QFileInfo(settings.fileName())
    print((settings.fileName()))
    print('lolo')
    if finfo.exists() and finfo.isFile():
        print('lolo')
        for w in qApp.allWidgets():
            mo = w.metaObject()
            if w.objectName() != "":
                for i in range(mo.propertyCount()):
                    name = mo.property(i).name()
                    val = settings.value("{}/{}".format(w.objectName(), name), w.property(name))
                    w.setProperty(name, val)
                    print('lolo')

def save(settings):
    print(settings.fileName())
    for w in qApp.allWidgets():
        mo = w.metaObject()
        if w.objectName() != "":
            for i in range(mo.propertyCount()):
                name = mo.property(i).name()
                #print(w.objectName())
                #print(w.property(name))
                settings.setValue("{}/{}".format(w.objectName(), name), w.property(name))

class Ui_MainWindow(QObject):
    #signals 
    takeTopLevel = pyqtSignal(int)
    takeBottomLevel = pyqtSignal(int)
    takeWVLeft = pyqtSignal(float)
    takeWVRight = pyqtSignal(float)
    takePointWVLeft =  pyqtSignal(int)
    takePointWVRight =  pyqtSignal(int)
    takeCalimPointLeft = pyqtSignal()
    takeCalimPointRight = pyqtSignal()
    takeFps = pyqtSignal(float)
    takeExposure = pyqtSignal(float)
    takeBoost = pyqtSignal(int)
    takeTriggerDelay = pyqtSignal(int)
    takeAvgVid = pyqtSignal(int)
    takePixTime = pyqtSignal(int)
    backUse = pyqtSignal(bool)
    SpecLog = pyqtSignal(bool)
    gainBoost = pyqtSignal(bool)
    trigger = pyqtSignal(bool)
    exposureMax = pyqtSignal(bool)
    startStop = pyqtSignal(bool)
    stageSetPosE = pyqtSignal(float)
    expStartSi = pyqtSignal(tuple)
    saveSi = pyqtSignal(str)
    takeStageVelocity = pyqtSignal(float)
    HRIInit = pyqtSignal(bool)
    takeMCP = pyqtSignal(int)
    takeHRIThr = pyqtSignal(int)
    
    settings = QSettings("gui.ini", QSettings.IniFormat)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1000)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        MainWindow.setWindowIcon(QtGui.QIcon('logo.png'))
        #video
        self.graphicsVideoL = QLabel(self.centralWidget)
        self.graphicsVideoL.setGeometry(QtCore.QRect(20, 2, imageSizeUIx, imageSizeUIy))
        self.graphicsVideoL.setObjectName("graphicsVideoL")

		#spectrum
        self.graphicsSpectrum = pg.PlotWidget(self.centralWidget)
        #self.graphicsSpectrum = QLabel(self.centralWidget)
        self.graphicsSpectrum.setGeometry(QtCore.QRect(20, 485, imageSizeUIx, imageSizeUIy - 40))
        self.graphicsSpectrum.setObjectName("graphicsSpectrum")
		
        #scan
        self.graphicsScan = pg.PlotWidget(self.centralWidget)
        self.graphicsScan.setGeometry(QtCore.QRect(1200, 610, imageSizeUIx/2, imageSizeUIy/2))
        self.graphicsScan.setObjectName("graphicsSpectrum")
        
        #self.graphicsSpectrum = QtWidgets.QGraphicsView(self.centralWidget)
        #self.graphicsSpectrum.setGeometry(QtCore.QRect(40, 310, 521, 281))
        #self.graphicsSpectrum.setObjectName("graphicsSpectrum")
		
		#parameters of the camera
        self.groupBoxCamParam = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBoxCamParam.setGeometry(QtCore.QRect(630, 10, 400, 170))
        self.groupBoxCamParam.setObjectName("groupBoxCamParam")

        self.checkBoxInitCam = QtWidgets.QCheckBox(self.groupBoxCamParam)
        self.checkBoxInitCam.setGeometry(QtCore.QRect(100, 30, 60, 20))
        self.checkBoxInitCam.setObjectName("labelInitCam")
        self.checkBoxInitCam.setText("init")
        
        self.labelStartStop = QtWidgets.QLabel(self.groupBoxCamParam)
        self.labelStartStop.setGeometry(QtCore.QRect(10, 30, 60, 20))
        self.labelStartStop.setObjectName("labelStartStop")

        self.checkBoxStartStop = QtWidgets.QCheckBox(self.groupBoxCamParam)
        self.checkBoxStartStop.setGeometry(QtCore.QRect(80, 30, 20, 20))
        self.checkBoxStartStop.setObjectName("checkBoxStartStop")
        
        self.labelFps = QtWidgets.QLabel(self.groupBoxCamParam)
        self.labelFps.setGeometry(QtCore.QRect(10, 50, 60, 20))
        self.labelFps.setObjectName("labelFps")
        self.labelExposure = QtWidgets.QLabel(self.groupBoxCamParam)
        self.labelExposure.setGeometry(QtCore.QRect(10, 70, 60, 20))
        self.labelExposure.setObjectName("labelExposure")
        
        self.labelExposureMax = QtWidgets.QLabel(self.groupBoxCamParam)
        self.labelExposureMax.setGeometry(QtCore.QRect(150, 70, 60, 20))
        self.labelExposureMax.setObjectName("labelExposureMax")
        
        self.checkBoxExposureMax = QtWidgets.QCheckBox(self.groupBoxCamParam)
        self.checkBoxExposureMax.setGeometry(QtCore.QRect(220, 70, 20, 20))
        self.checkBoxExposureMax.setObjectName("checkBoxExposureMax")
        
        self.labelBoost = QtWidgets.QLabel(self.groupBoxCamParam)
        self.labelBoost.setGeometry(QtCore.QRect(10, 90, 60, 20))
        self.labelBoost.setObjectName("labelBoost")
        
        self.labelGainBoost = QtWidgets.QLabel(self.groupBoxCamParam)
        self.labelGainBoost.setGeometry(QtCore.QRect(150, 90, 60, 20))
        self.labelGainBoost.setObjectName("labelGainBoost")
        
        self.spinBoxFps = QtWidgets.QDoubleSpinBox(self.groupBoxCamParam)
        self.spinBoxFps.setMaximum(10000000)
        self.spinBoxFps.setGeometry(QtCore.QRect(80, 50, 60, 20))
        self.spinBoxFps.setValue(20)
        self.spinBoxFps.setSingleStep(1)
        self.spinBoxFps.setObjectName("spinBoxFps")
        
        self.labelTrigger = QtWidgets.QLabel(self.groupBoxCamParam)
        self.labelTrigger.setGeometry(QtCore.QRect(150, 50, 65, 20))
        self.labelTrigger.setObjectName("labelTrigger")
        
        self.checkBoxTrigger = QtWidgets.QCheckBox(self.groupBoxCamParam)
        self.checkBoxTrigger.setGeometry(QtCore.QRect(220, 50, 20, 20))
        self.checkBoxTrigger.setObjectName("checkBoxTrigger")
        
        self.labelTriggerDelay = QtWidgets.QLabel(self.groupBoxCamParam)
        self.labelTriggerDelay.setGeometry(QtCore.QRect(250, 50, 35, 20))
        self.labelTriggerDelay.setObjectName("labelTriggerDelay")
        
        self.spinBoxTriggerDelay = QtWidgets.QDoubleSpinBox(self.groupBoxCamParam)
        self.spinBoxTriggerDelay.setMaximum(100000)
        self.spinBoxTriggerDelay.setGeometry(QtCore.QRect(290, 50, 100, 20))
        self.spinBoxTriggerDelay.setValue(9960)
        self.spinBoxTriggerDelay.setObjectName("spinBoxTriggerDelay")
        
        self.spinBoxExposure = QtWidgets.QDoubleSpinBox(self.groupBoxCamParam)
        self.spinBoxExposure.setMaximum(10000000)
        self.spinBoxExposure.setMinimum(1)
        self.spinBoxExposure.setGeometry(QtCore.QRect(80, 70, 60, 20))
        self.spinBoxExposure.setValue(20000)
        self.spinBoxExposure.setObjectName("spinBoxExposure")
        self.spinBoxExposure.setSingleStep(1)
        self.spinBoxBoost = QtWidgets.QDoubleSpinBox(self.groupBoxCamParam)
        self.spinBoxBoost.setMaximum(36)
        self.spinBoxBoost.setMinimum(0)
        self.spinBoxBoost.setGeometry(QtCore.QRect(80, 90, 60, 20))
        self.spinBoxBoost.setValue(0)
        self.spinBoxBoost.setObjectName("spinBoxBoost")
        self.spinBoxBoost.setSingleStep(0.1)
        self.checkBoxGainBoost = QtWidgets.QCheckBox(self.groupBoxCamParam)
        self.checkBoxGainBoost.setGeometry(QtCore.QRect(220, 90, 20, 20))
        self.checkBoxGainBoost.setObjectName("checkBoxGainBoost")
        
        self.labelAvgVid = QtWidgets.QLabel(self.groupBoxCamParam)
        self.labelAvgVid.setGeometry(QtCore.QRect(10, 110, 60, 20))
        self.labelAvgVid.setObjectName("labelAvgVid")

        self.spinBoxAvgVid = QtWidgets.QSpinBox(self.groupBoxCamParam)
        self.spinBoxAvgVid.setMaximum(1000)
        self.spinBoxAvgVid.setGeometry(QtCore.QRect(80, 110, 60, 20))
        self.spinBoxAvgVid.setValue(1)
        self.spinBoxAvgVid.setObjectName("spinBoxAvgVid")
        self.spinBoxAvgVid.setSingleStep(1)
        
        self.labelPixTime = QtWidgets.QLabel(self.groupBoxCamParam)
        self.labelPixTime.setGeometry(QtCore.QRect(10, 130, 60, 20))
        self.labelPixTime.setObjectName("labelPixTime")
        
        self.spinBoxPixTime = QtWidgets.QSpinBox(self.groupBoxCamParam)
        self.spinBoxPixTime.setMaximum(1000)
        self.spinBoxPixTime.setGeometry(QtCore.QRect(80, 130, 60, 20))
        self.spinBoxPixTime.setValue(0)
        self.spinBoxPixTime.setObjectName("spinBoxPixTime")
        self.spinBoxPixTime.setSingleStep(1)
        
        self.checkBoxImQual = QtWidgets.QCheckBox(self.groupBoxCamParam)
        self.checkBoxImQual.setText("change Qual")
        self.checkBoxImQual.setGeometry(QtCore.QRect(160, 130, 100, 22))
        
		#lines for area
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(630, 170, 311, 81))
        self.groupBox.setObjectName("areaForSpec")
        self.spinBoxBottom = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxBottom.setMaximum(10000)
        self.spinBoxBottom.setGeometry(QtCore.QRect(63, 50, 60, 22))
        self.spinBoxBottom.setValue(10)
        self.spinBoxBottom.setObjectName("spinBoxBottom")
        self.spinBoxTop = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxTop.setMaximum(10000)
        self.spinBoxTop.setGeometry(QtCore.QRect(63, 20, 60, 22))
        self.spinBoxTop.setValue(470)
        self.spinBoxTop.setObjectName("spinBoxTop")
        self.spinBoxLeft = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxLeft.setGeometry(QtCore.QRect(170, 20, 42, 22))
        self.spinBoxLeft.setObjectName("spinBoxLeft")
        self.spinBoxLeft.setMaximum(10000)
        self.spinBoxRight = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxRight.setGeometry(QtCore.QRect(170, 50, 42, 22))
        self.spinBoxRight.setObjectName("spinBoxRight") 
        self.spinBoxRight.setMaximum(10000)
        
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 50, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 50, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(120, 20, 50, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(120, 50, 50, 17))
        self.label_4.setObjectName("label_4")

        #calibration
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_3.setGeometry(QtCore.QRect(630, 250, 311, 151))
        self.groupBox_3.setObjectName("calibration")
		
        self.pushButtonTakeLeftPoint = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButtonTakeLeftPoint.setGeometry(QtCore.QRect(10, 30, 101, 23))
        self.pushButtonTakeLeftPoint.setObjectName("pushButtonTakeLeftPoint")
		
        self.pushButtonTakeRightPoint = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButtonTakeRightPoint.setGeometry(QtCore.QRect(160, 30, 101, 23))
        self.pushButtonTakeRightPoint.setObjectName("pushButtonTakeRightPoint")
		
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setGeometry(QtCore.QRect(10, 60, 61, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(160, 60, 61, 16))
        self.label_7.setObjectName("label_7")
		
        self.labelLeftPoint = QtWidgets.QLabel(self.groupBox_3)
        self.labelLeftPoint.setGeometry(QtCore.QRect(10, 90, 61, 16))
        self.labelLeftPoint.setObjectName("labelLeftPoint")
        self.labelRightPoint = QtWidgets.QLabel(self.groupBox_3)
        self.labelRightPoint.setGeometry(QtCore.QRect(160, 90, 61, 16))
        self.labelRightPoint.setObjectName("labelRightPoint")
		
        self.spinBoxPointWLLeft = QtWidgets.QSpinBox(self.groupBox_3)
        self.spinBoxPointWLLeft.setGeometry(QtCore.QRect(80, 60, 70, 22))
        self.spinBoxPointWLLeft.setObjectName("spinBoxCalibrationLeft")
        self.spinBoxPointWLLeft.setMaximum(10000)
        self.spinBoxPointWLLeft.setValue(20)
		
        self.spinBoxPointWLRight = QtWidgets.QSpinBox(self.groupBox_3)
        self.spinBoxPointWLRight.setGeometry(QtCore.QRect(230, 60, 70, 22))
        self.spinBoxPointWLRight.setObjectName("spinBox_3")
        self.spinBoxPointWLRight.setMaximum(10000)
        self.spinBoxPointWLRight.setValue(580)
		
        self.doubleSpinBoxWLLeft = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBoxWLLeft.setGeometry(QtCore.QRect(80, 90, 70, 22))
        self.doubleSpinBoxWLLeft.setObjectName("doubleSpinBoxWLLeft")
        self.doubleSpinBoxWLLeft.setMaximum(2000)
        self.doubleSpinBoxWLLeft.setValue(580)
		
        self.doubleSpinBoxWLRight = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBoxWLRight.setGeometry(QtCore.QRect(230, 90, 70, 22))
        self.doubleSpinBoxWLRight.setObjectName("doubleSpinBoxWLRight")
        self.doubleSpinBoxWLRight.setMaximum(2000)
        
        #spectum... photo and cut
        self.groupBoxSpec = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBoxSpec.setGeometry(QtCore.QRect(630, 400, 311, 250))
        self.groupBoxSpec.setObjectName("calibration")
        
        self.pushButtonSave = QtWidgets.QPushButton(self.groupBoxSpec)
        self.pushButtonSave.setText("save")
        self.pushButtonSave.setGeometry(QtCore.QRect(20, 40, 100, 22))
        
        self.pushButtonBackTake = QtWidgets.QPushButton(self.groupBoxSpec)
        self.pushButtonBackTake.setText("take background")
        self.pushButtonBackTake.setGeometry(QtCore.QRect(20, 70, 100, 22))   
        
        #self.labelBackGTake = QtWidgets.QLabel(self.groupBoxSpec)
        #self.labelBackGTake.setGeometry(QtCore.QRect(20, 70, 130, 20))
        #self.labelBackGTake.setObjectName("labelBackGTake")
        #self.labelBackGTake.setText("take background")        

        #self.checkBoxBackGTake = QtWidgets.QCheckBox(self.groupBoxSpec)
        #self.checkBoxBackGTake.setGeometry(QtCore.QRect(140, 70, 20, 20))
        #self.checkBoxBackGTake.setObjectName("checkBoxBackGTake")

        self.labelBackGUse = QtWidgets.QLabel(self.groupBoxSpec)
        self.labelBackGUse.setGeometry(QtCore.QRect(20, 100, 130, 20))
        self.labelBackGUse.setObjectName("labelBackGUse")
        self.labelBackGUse.setText("use background")      
        
        self.checkBoxBackGUse = QtWidgets.QCheckBox(self.groupBoxSpec)
        self.checkBoxBackGUse.setGeometry(QtCore.QRect(140, 100, 20, 20))
        self.checkBoxBackGUse.setObjectName("checkBoxBackGUse")
        
        self.labelSpecLog1 = QtWidgets.QLabel(self.groupBoxSpec)
        self.labelSpecLog1.setGeometry(QtCore.QRect(20, 160, 130, 20))
        self.labelSpecLog1.setObjectName("labelSpecLog1")
        self.labelSpecLog1.setText("set log scale") 

        self.checkBoxSpecLog1 = QtWidgets.QCheckBox(self.groupBoxSpec)
        self.checkBoxSpecLog1.setGeometry(QtCore.QRect(140, 160, 20, 20))
        self.checkBoxSpecLog1.setObjectName("checkBoxSpecLog1")
        
        self.labelSpecLog = QtWidgets.QLabel(self.groupBoxSpec)
        self.labelSpecLog.setGeometry(QtCore.QRect(20, 130, 130, 20))
        self.labelSpecLog.setObjectName("labelSpecLog")
        self.labelSpecLog.setText("add transmission")     
        
        self.checkBoxSpecLog = QtWidgets.QCheckBox(self.groupBoxSpec)
        self.checkBoxSpecLog.setGeometry(QtCore.QRect(140, 130, 20, 20))
        self.checkBoxSpecLog.setObjectName("checkBoxSpecLog")
        
        #Stage
        self.groupBoxStage = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBoxStage.setGeometry(QtCore.QRect(630, 650, 311, 120))
        self.groupBoxStage.setObjectName("calibration")
        self.groupBoxStage.setTitle("stage control")
        
        self.labelPosition = QtWidgets.QLabel(self.groupBoxStage)
        self.labelPosition.setGeometry(QtCore.QRect(20, 30, 50, 20))
        self.labelPosition.setObjectName("labelPosition")
        self.labelPosition.setText("position")   
        
        self.labelPositionShow = QtWidgets.QLabel(self.groupBoxStage)
        self.labelPositionShow.setGeometry(QtCore.QRect(150, 30, 50, 20))
        self.labelPositionShow.setObjectName("labelPositionShow")
        self.labelPositionShow.setText("1")   
        
        #self.labelPositionSet = QtWidgets.QLabel(self.groupBoxStage)
        #self.labelPositionSet.setGeometry(QtCore.QRect(20, 30, 50, 20))
        #self.labelPositionSet.setObjectName("labelPositionSet")
        #self.labelPositionSet.setText("position")   
        
        self.pushButtonStagePosSet = QtWidgets.QPushButton(self.groupBoxStage)
        self.pushButtonStagePosSet.setGeometry(QtCore.QRect(20, 50, 50, 20))
        self.pushButtonStagePosSet.setObjectName("pushButtonStagePosSet")
        self.pushButtonStagePosSet.setText("set pos")
        
        self.spinBoxPosition = QtWidgets.QDoubleSpinBox(self.groupBoxStage)
        self.spinBoxPosition.setGeometry(QtCore.QRect(150, 50, 80, 22))
        self.spinBoxPosition.setObjectName("spinBoxPosition")
        self.spinBoxPosition.setMaximum(24)
        self.spinBoxPosition.setSingleStep(0.00005)
        self.spinBoxPosition.setDecimals(5)
        self.spinBoxPosition.setValue(10)

        self.labelStageVelocity = QtWidgets.QLabel(self.groupBoxStage)
        self.labelStageVelocity.setGeometry(QtCore.QRect(20, 70, 50, 20))
        self.labelStageVelocity.setObjectName("labelStageVelocity")
        self.labelStageVelocity.setText("velocity")   
        
        self.spinBoxStageVelocity = QtWidgets.QDoubleSpinBox(self.groupBoxStage)
        self.spinBoxStageVelocity.setGeometry(QtCore.QRect(150, 70, 80, 22))
        self.spinBoxStageVelocity.setObjectName("spinBoxStageVelocity")
        self.spinBoxStageVelocity.setMaximum(2.4)
        self.spinBoxStageVelocity.setSingleStep(0.000050)
        self.spinBoxStageVelocity.setDecimals(6)
        self.spinBoxStageVelocity.setValue(2.3)
        
        self.checkBoxInitStage = QtWidgets.QCheckBox(self.groupBoxStage)
        self.checkBoxInitStage.setGeometry(QtCore.QRect(150, 90, 80, 22))
        self.checkBoxInitStage.setObjectName("checkBoxInitStage")
        self.checkBoxInitStage.setText('init')
        
        self.pushButtonStageHome = QtWidgets.QPushButton(self.groupBoxStage)
        self.pushButtonStageHome.setGeometry(QtCore.QRect(20, 90, 50, 20))
        self.pushButtonStageHome.setObjectName("pushButtonStageHome")
        self.pushButtonStageHome.setText("home")

        #experiment!!!
        self.groupExp = QtWidgets.QGroupBox(self.centralWidget)
        self.groupExp.setGeometry(QtCore.QRect(630, 780, 311, 100))
        self.groupExp.setObjectName("groupExp")
        self.groupExp.setTitle("experiment")
        
        self.labelExpStartPos = QtWidgets.QLabel(self.groupExp)
        self.labelExpStartPos.setGeometry(QtCore.QRect(20, 30, 150, 20))
        self.labelExpStartPos.setObjectName("labelExpStartPos")
        self.labelExpStartPos.setText("start position")   
        
        self.spinBoxExpStartPos = QtWidgets.QDoubleSpinBox(self.groupExp)
        self.spinBoxExpStartPos.setGeometry(QtCore.QRect(150, 30, 80, 22))
        self.spinBoxExpStartPos.setObjectName("spinBoxExpStartPos")
        self.spinBoxExpStartPos.setMaximum(24)
        self.spinBoxExpStartPos.setSingleStep(0.001)
        self.spinBoxExpStartPos.setDecimals(5)
        self.spinBoxExpStartPos.setValue(10)
        
        self.labelExpStopPos = QtWidgets.QLabel(self.groupExp)
        self.labelExpStopPos.setGeometry(QtCore.QRect(20, 60, 150, 20))
        self.labelExpStopPos.setObjectName("labelExpStopPos")
        self.labelExpStopPos.setText("stop position")   
        
        self.spinBoxExpStopPos = QtWidgets.QDoubleSpinBox(self.groupExp)
        self.spinBoxExpStopPos.setGeometry(QtCore.QRect(150, 60, 80, 22))
        self.spinBoxExpStopPos.setObjectName("spinBoxExpStopPos")
        self.spinBoxExpStopPos.setMaximum(24)
        self.spinBoxExpStopPos.setSingleStep(0.001)
        self.spinBoxExpStopPos.setDecimals(5)
        self.spinBoxExpStopPos.setValue(10.200)

        self.pushButtonExpStart = QtWidgets.QPushButton(self.groupExp)
        self.pushButtonExpStart.setGeometry(QtCore.QRect(235, 30, 75, 23))
        self.pushButtonExpStart.setObjectName("pushButtonExpStart")
        self.pushButtonExpStart.setText("start")
        
        #HRI!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.groupBoxHRI = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBoxHRI.setGeometry(QtCore.QRect(1050, 10, 291, 261))
        self.groupBoxHRI.setObjectName("groupBoxHRI")
        self.groupBoxHRI.setTitle("HRI")
        
        self.pushButtonRemote = QtWidgets.QPushButton(self.groupBoxHRI)
        self.pushButtonRemote.setGeometry(QtCore.QRect(10, 30, 75, 23))
        self.pushButtonRemote.setObjectName("pushButtonRemote")
        self.pushButtonRemote.setText("Remote")
        
        
        self.pushButtonLocal = QtWidgets.QPushButton(self.groupBoxHRI)
        self.pushButtonLocal.setGeometry(QtCore.QRect(110, 30, 75, 23))
        self.pushButtonLocal.setObjectName("pushButtonLocal")
        self.pushButtonLocal.setText("Local")
        
        self.labelHRIMode = QtWidgets.QLabel(self.groupBoxHRI)
        self.labelHRIMode.setGeometry(QtCore.QRect(20, 60, 47, 13))
        self.labelHRIMode.setObjectName("labelHRIMode")
        self.labelHRIMode.setText("Mode")
        
        self.comboBoxMode = QtWidgets.QComboBox(self.groupBoxHRI)
        self.comboBoxMode.setGeometry(QtCore.QRect(110, 60, 161, 22))
        self.comboBoxMode.setObjectName("comboBoxMode")
        self.comboBoxMode.addItem("Inhibit")
        self.comboBoxMode.addItem("<50ps comb")
        self.comboBoxMode.addItem("50ps comb")
        self.comboBoxMode.addItem("100ps comb")
        self.comboBoxMode.addItem("150ps comb")
        self.comboBoxMode.addItem("200ps comb")
        self.comboBoxMode.addItem("1000ps comb")
        self.comboBoxMode.addItem("2000ps comb")
        self.comboBoxMode.addItem("3000ps comb")
        self.comboBoxMode.addItem("4000ps comb")
        self.comboBoxMode.addItem("5000ps comb")
        self.comboBoxMode.addItem("DC")
        
        self.labelMCP = QtWidgets.QLabel(self.groupBoxHRI)
        self.labelMCP.setGeometry(QtCore.QRect(20, 90, 47, 13))
        self.labelMCP.setObjectName("labelMCP")
        self.labelMCP.setText("MCP V")
        
        
        self.labelHRIThr = QtWidgets.QLabel(self.groupBoxHRI)
        self.labelHRIThr.setGeometry(QtCore.QRect(20, 120, 47, 13))
        self.labelHRIThr.setObjectName("labelHRIThr")
        self.labelHRIThr.setText("thresh")
        
        self.lcdNumber = QtWidgets.QLCDNumber(self.groupBoxHRI)
        self.lcdNumber.setGeometry(QtCore.QRect(210, 30, 64, 23))
        self.lcdNumber.setObjectName("lcdNumber")
        
        self.doubleSpinMCP = QtWidgets.QDoubleSpinBox(self.groupBoxHRI)
        self.doubleSpinMCP.setGeometry(QtCore.QRect(110, 90, 62, 22))
        self.doubleSpinMCP.setObjectName("doubleSpinMCP")
        self.doubleSpinMCP.setMaximum(800)
        self.doubleSpinMCP.setMinimum(260)
        self.doubleSpinMCP.setSingleStep(5)
        #self.doubleSpinMCP.setDecimals(5)
        self.doubleSpinMCP.setValue(260)
        
        self.doubleSpinBoxHRIThr = QtWidgets.QDoubleSpinBox(self.groupBoxHRI)
        self.doubleSpinBoxHRIThr.setGeometry(QtCore.QRect(110, 120, 62, 22))
        self.doubleSpinBoxHRIThr.setObjectName("doubleSpinBoxHRIThr")
        self.doubleSpinBoxHRIThr.setMaximum(230)
        self.doubleSpinBoxHRIThr.setMinimum(0)
        self.doubleSpinBoxHRIThr.setSingleStep(1)
        #self.doubleSpinMCP.setDecimals(5)
        self.doubleSpinBoxHRIThr.setValue(40)
        
        self.pushButton50Trig = QtWidgets.QPushButton(self.groupBoxHRI)
        self.pushButton50Trig.setGeometry(QtCore.QRect(10, 150, 75, 23))
        self.pushButton50Trig.setObjectName("pushButton50Trig")
        self.pushButton50Trig.setText('Trig 50')
        
        self.pushButtonHiTrig = QtWidgets.QPushButton(self.groupBoxHRI)
        self.pushButtonHiTrig.setGeometry(QtCore.QRect(110, 150, 75, 23))
        self.pushButtonHiTrig.setObjectName("pushButtonHiTrig")
        self.pushButtonHiTrig.setText('Hi Trig')
        
        self.pushButtonPosTrig = QtWidgets.QPushButton(self.groupBoxHRI)
        self.pushButtonPosTrig.setGeometry(QtCore.QRect(10, 180, 75, 23))
        self.pushButtonPosTrig.setObjectName("pushButtonPosTrig")
        self.pushButtonPosTrig.setText('+ Trig')
        
        self.pushButtonNegTrig = QtWidgets.QPushButton(self.groupBoxHRI)
        self.pushButtonNegTrig.setGeometry(QtCore.QRect(110, 180, 75, 23))
        self.pushButtonNegTrig.setObjectName("pushButtonNegTrig")
        self.pushButtonNegTrig.setText('- Trig')

        self.pushButtonStat = QtWidgets.QPushButton(self.groupBoxHRI)
        self.pushButtonStat.setGeometry(QtCore.QRect(10, 210, 75, 23))
        self.pushButtonStat.setObjectName("pushButtonStat")
        self.pushButtonStat.setText('Status')
        
        self.pushButtonRev = QtWidgets.QPushButton(self.groupBoxHRI)
        self.pushButtonRev.setGeometry(QtCore.QRect(110, 210, 75, 23))
        self.pushButtonRev.setObjectName("pushButtonRev")
        self.pushButtonRev.setText('Rev')
        
        self.labelInit = QtWidgets.QLabel(self.groupBoxHRI)
        self.labelInit.setGeometry(QtCore.QRect(200, 180, 75, 20))
        self.labelInit.setObjectName("labelInit")
        self.labelInit.setText("Initializzze")

        self.checkBoxInit = QtWidgets.QCheckBox(self.groupBoxHRI)
        self.checkBoxInit.setGeometry(QtCore.QRect(200, 210, 20, 20))
        self.checkBoxInit.setObjectName("checkBoxInit")
        self.checkBoxInit.setText("init")
        
        # P400!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.groupBoxDG = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBoxDG.setGeometry(QtCore.QRect(1050, 280, 241, 321))
        self.groupBoxDG.setObjectName("groupBoxDG")
        self.groupBoxDG.setTitle('P400')
        
        self.tabWidgetDG = QtWidgets.QTabWidget(self.groupBoxDG)
        self.tabWidgetDG.setGeometry(QtCore.QRect(0, 70, 241, 251))
        self.tabWidgetDG.setObjectName("tabWidgetDG")
        
        self.tabTrigger = QtWidgets.QWidget()
        self.tabTrigger.setObjectName("tabTrigger")
        
        self.labelDGSource = QtWidgets.QLabel(self.tabTrigger)
        self.labelDGSource.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.labelDGSource.setObjectName("labelDGSource")
        
        self.comboBoxDGSource = QtWidgets.QComboBox(self.tabTrigger)
        self.comboBoxDGSource.setGeometry(QtCore.QRect(70, 10, 69, 22))
        self.comboBoxDGSource.setObjectName("comboBoxDGSource")
        self.comboBoxDGSource.addItem("Ext")
        self.comboBoxDGSource.addItem("MAN")
        self.comboBoxDGSource.addItem("INT")     
        self.comboBoxDGSource.addItem("LINE")
        self.comboBoxDGSource.addItem("REM")
        
        self.labelDGEdge = QtWidgets.QLabel(self.tabTrigger)
        self.labelDGEdge.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.labelDGEdge.setObjectName("labelDGEdge")
        
        self.labelDGTerm = QtWidgets.QLabel(self.tabTrigger)
        self.labelDGTerm.setGeometry(QtCore.QRect(10, 70, 47, 13))
        self.labelDGTerm.setObjectName("labelDGTerm")
        
        self.labelDGLvl = QtWidgets.QLabel(self.tabTrigger)
        self.labelDGLvl.setGeometry(QtCore.QRect(10, 100, 47, 13))
        self.labelDGLvl.setObjectName("labelDGLvl")
        
        self.labelDGGateMode = QtWidgets.QLabel(self.tabTrigger)
        self.labelDGGateMode.setGeometry(QtCore.QRect(10, 130, 61, 16))
        self.labelDGGateMode.setObjectName("labelDGGateMode")
        
        self.comboBoxDGEdge = QtWidgets.QComboBox(self.tabTrigger)
        self.comboBoxDGEdge.setGeometry(QtCore.QRect(70, 40, 69, 22))
        self.comboBoxDGEdge.setObjectName("comboBoxDGEdge")
        self.comboBoxDGEdge.addItem("POS")
        self.comboBoxDGEdge.addItem("NEG")
        
        self.comboBoxDGTerm = QtWidgets.QComboBox(self.tabTrigger)
        self.comboBoxDGTerm.setGeometry(QtCore.QRect(70, 70, 69, 22))
        self.comboBoxDGTerm.setObjectName("comboBoxDGTerm")
        self.comboBoxDGTerm.addItem("50OHM")
        self.comboBoxDGTerm.addItem("HIGHZ")
        
        self.comboBoxDGGateMode = QtWidgets.QComboBox(self.tabTrigger)
        self.comboBoxDGGateMode.setGeometry(QtCore.QRect(70, 130, 69, 22))
        self.comboBoxDGGateMode.setObjectName("comboBoxDGGateMode")
        self.comboBoxDGGateMode.addItem("1")
        self.comboBoxDGGateMode.addItem("2")
        self.comboBoxDGGateMode.addItem("3")
        self.comboBoxDGGateMode.addItem("4")
        
        self.doubleSpinBoxDGLvl = QtWidgets.QDoubleSpinBox(self.tabTrigger)
        self.doubleSpinBoxDGLvl.setGeometry(QtCore.QRect(70, 100, 71, 22))
        self.doubleSpinBoxDGLvl.setObjectName("doubleSpinBoxDGLvl")
        self.doubleSpinBoxDGLvl.setMaximum(4.6)
        self.doubleSpinBoxDGLvl.setMinimum(-2.4)
        self.doubleSpinBoxDGLvl.setSingleStep(0.1)
        #self.doubleSpinMCP.setDecimals(5)
        self.doubleSpinBoxDGLvl.setValue(0.6)
        #channel A!!!!!!!!!!!!!!!!!!!!!!!!@!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.tabWidgetDG.addTab(self.tabTrigger, "")
        
        self.tabChA = QtWidgets.QWidget()
        self.tabChA.setObjectName("tabChA")
        
        self.labelDGAdelay = QtWidgets.QLabel(self.tabChA)
        self.labelDGAdelay.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.labelDGAdelay.setObjectName("labelDGAdelay")
        self.labelDGADelayStep = QtWidgets.QLabel(self.tabChA)
        self.labelDGADelayStep.setGeometry(QtCore.QRect(10, 40, 51, 16))
        self.labelDGADelayStep.setObjectName("labelDGADelayStep")
        self.labelDGARefCh = QtWidgets.QLabel(self.tabChA)
        self.labelDGARefCh.setGeometry(QtCore.QRect(10, 70, 47, 13))
        self.labelDGARefCh.setObjectName("labelDGARefCh")
        self.labelDGAPol = QtWidgets.QLabel(self.tabChA)
        self.labelDGAPol.setGeometry(QtCore.QRect(10, 130, 47, 13))
        self.labelDGAPol.setObjectName("labelDGAPol")
        self.labelDGAVHigh = QtWidgets.QLabel(self.tabChA)
        self.labelDGAVHigh.setGeometry(QtCore.QRect(10, 160, 47, 13))
        self.labelDGAVHigh.setObjectName("labelDGAVHigh")
        self.labelDGAVLow = QtWidgets.QLabel(self.tabChA)
        self.labelDGAVLow.setGeometry(QtCore.QRect(10, 190, 47, 16))
        self.labelDGAVLow.setObjectName("labelDGAVLow")
        
        self.doubleSpinBoxDGAdelay = QtWidgets.QDoubleSpinBox(self.tabChA)
        self.doubleSpinBoxDGAdelay.setGeometry(QtCore.QRect(70, 10, 141, 22))
        self.doubleSpinBoxDGAdelay.setObjectName("doubleSpinBoxDGAdelay")
        self.doubleSpinBoxDGAdelay.setMaximum(+999999999999999)
        self.doubleSpinBoxDGAdelay.setMinimum(-999999999999999)
        self.doubleSpinBoxDGAdelay.setSingleStep(1)
        self.doubleSpinBoxDGAdelay.setValue(0)
        
        self.doubleSpinBoxDGADelayStep = QtWidgets.QDoubleSpinBox(self.tabChA)
        self.doubleSpinBoxDGADelayStep.setGeometry(QtCore.QRect(70, 40, 141, 22))
        self.doubleSpinBoxDGADelayStep.setObjectName("doubleSpinBoxDGADelayStep")
        self.doubleSpinBoxDGADelayStep.setMaximum(+999999999999999)
        self.doubleSpinBoxDGADelayStep.setMinimum(1)
        self.doubleSpinBoxDGADelayStep.setSingleStep(1)
        self.doubleSpinBoxDGADelayStep.setValue(1)
        self.doubleSpinBoxDGADelayStep.valueChanged.connect(self.doubleSpinBoxDGAdelay.setSingleStep)
        
        self.doubleSpinBoxDGAVHigh = QtWidgets.QDoubleSpinBox(self.tabChA)
        self.doubleSpinBoxDGAVHigh.setGeometry(QtCore.QRect(70, 160, 71, 22))
        self.doubleSpinBoxDGAVHigh.setObjectName("doubleSpinBoxDGAVHigh")
        self.doubleSpinBoxDGAVHigh.setMaximum(+11.80)
        self.doubleSpinBoxDGAVHigh.setMinimum(-4.30)
        self.doubleSpinBoxDGAVHigh.setSingleStep(0.10)
        self.doubleSpinBoxDGAVHigh.setValue(2)
        
        self.doubleSpinBoxDGAVLow = QtWidgets.QDoubleSpinBox(self.tabChA)
        self.doubleSpinBoxDGAVLow.setGeometry(QtCore.QRect(70, 190, 71, 22))
        self.doubleSpinBoxDGAVLow.setObjectName("doubleSpinBoxDGAVLow")
        self.doubleSpinBoxDGAVLow.setMaximum(+4.10)
        self.doubleSpinBoxDGAVLow.setMinimum(-5.00)
        self.doubleSpinBoxDGAVLow.setSingleStep(0.10)
        self.doubleSpinBoxDGAVLow.setValue(0)
        
        self.comboBoxDGARefCh = QtWidgets.QComboBox(self.tabChA)
        self.comboBoxDGARefCh.setGeometry(QtCore.QRect(70, 70, 69, 22))
        self.comboBoxDGARefCh.setObjectName("comboBoxDGARefCh")
        self.comboBoxDGARefCh.addItem("0")
        self.comboBoxDGARefCh.addItem("1")
        self.comboBoxDGARefCh.addItem("2")
        self.comboBoxDGARefCh.addItem("3")
        self.comboBoxDGARefCh.addItem("4")
        self.comboBoxDGARefCh.addItem("5")
        self.comboBoxDGARefCh.addItem("6")
        self.comboBoxDGARefCh.addItem("7")
        self.comboBoxDGARefCh.addItem("8")
        
        self.comboBoxDGAPol = QtWidgets.QComboBox(self.tabChA)
        self.comboBoxDGAPol.setGeometry(QtCore.QRect(70, 130, 69, 22))
        self.comboBoxDGAPol.setObjectName("comboBoxDGAPol")
        self.comboBoxDGAPol.addItem("POS")
        self.comboBoxDGAPol.addItem("NEG")
        #??????????????????????what is width
        self.doubleSpinBoxDGAWidth = QtWidgets.QDoubleSpinBox(self.tabChA)
        self.doubleSpinBoxDGAWidth.setGeometry(QtCore.QRect(70, 100, 141, 22))
        self.doubleSpinBoxDGAWidth.setObjectName("doubleSpinBoxDGAWidth")
        self.doubleSpinBoxDGAWidth.setMaximum(+999999999999999)
        self.doubleSpinBoxDGAWidth.setMinimum(0)
        #self.doubleSpinBoxDGADelayStep.setSingleStep(1)
        self.doubleSpinBoxDGAWidth.setValue(5000)
        
        self.labelDGAWidth = QtWidgets.QLabel(self.tabChA)
        self.labelDGAWidth.setGeometry(QtCore.QRect(10, 100, 47, 13))
        self.labelDGAWidth.setObjectName("labelDGAWidth")
        
        self.checkBoxDGAOn = QtWidgets.QCheckBox(self.tabChA)
        self.checkBoxDGAOn.setGeometry(QtCore.QRect(160, 200, 70, 17))
        self.checkBoxDGAOn.setObjectName("checkBoxDGAOn")
        
        self.tabWidgetDG.addTab(self.tabChA, "")
        
        self.lcdNumberDG = QtWidgets.QLCDNumber(self.groupBoxDG)
        self.lcdNumberDG.setGeometry(QtCore.QRect(170, 20, 64, 23))
        self.lcdNumberDG.setObjectName("lcdNumberDG")
        
        self.checkBoxDGStart = QtWidgets.QCheckBox(self.groupBoxDG)
        self.checkBoxDGStart.setGeometry(QtCore.QRect(10, 50, 70, 17))
        self.checkBoxDGStart.setObjectName("checkBoxDGStart")
        
        self.checkBoxDGInit = QtWidgets.QCheckBox(self.groupBoxDG)
        self.checkBoxDGInit.setGeometry(QtCore.QRect(10, 30, 70, 17))
        self.checkBoxDGInit.setObjectName("checkBoxDGInit")
        self.checkBoxDGInit.stateChanged.connect(self.lcdNumberDG.display)
        #scan!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.groupBoxScan = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBoxScan.setGeometry(QtCore.QRect(1050, 610, 131, 201))
        self.groupBoxScan.setObjectName("groupBoxScan")
        self.pushButtonScanStart = QtWidgets.QPushButton(self.groupBoxScan)
        self.pushButtonScanStart.setGeometry(QtCore.QRect(10, 110, 75, 23))
        self.pushButtonScanStart.setObjectName("pushButtonScanStart")
        
        self.labelScanStart = QtWidgets.QLabel(self.groupBoxScan)
        self.labelScanStart.setGeometry(QtCore.QRect(10, 20, 47, 13))
        self.labelScanStart.setObjectName("labelScanStart")
        self.doubleSpinBoxScanStart = QtWidgets.QDoubleSpinBox(self.groupBoxScan)
        self.doubleSpinBoxScanStart.setGeometry(QtCore.QRect(60, 20, 62, 22))
        self.doubleSpinBoxScanStart.setObjectName("doubleSpinBoxScanStart")
        
        self.labelScanStop = QtWidgets.QLabel(self.groupBoxScan)
        self.labelScanStop.setGeometry(QtCore.QRect(10, 50, 47, 13))
        self.labelScanStop.setObjectName("labelScanStop")
        self.doubleSpinBoxScanStop = QtWidgets.QDoubleSpinBox(self.groupBoxScan)
        self.doubleSpinBoxScanStop.setGeometry(QtCore.QRect(60, 50, 62, 22))
        self.doubleSpinBoxScanStop.setObjectName("doubleSpinBoxScanStop")
        
        self.labelScanStep = QtWidgets.QLabel(self.groupBoxScan)
        self.labelScanStep.setGeometry(QtCore.QRect(10, 80, 47, 13))
        self.labelScanStep.setObjectName("labelScanStep")
        self.doubleSpinBoxScanStep = QtWidgets.QDoubleSpinBox(self.groupBoxScan)
        self.doubleSpinBoxScanStep.setGeometry(QtCore.QRect(60, 80, 62, 22))
        self.doubleSpinBoxScanStep.setObjectName("doubleSpinBoxScanStep")
        self.pushButtonScanOnPlaceStart = QtWidgets.QPushButton(self.groupBoxScan)
        self.pushButtonScanOnPlaceStart.setGeometry(QtCore.QRect(10, 140, 75, 23))
        self.pushButtonScanOnPlaceStart.setObjectName("pushButtonScanOnPlaceStart")
        self.pushButtonScanSave = QtWidgets.QPushButton(self.groupBoxScan)
        self.pushButtonScanSave.setGeometry(QtCore.QRect(10, 170, 75, 23))
        self.pushButtonScanSave.setObjectName("pushButtonScanSave")
        
        #menu
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1063, 21))
        self.menuBar.setObjectName("menuBar")
        self.menufile = QtWidgets.QMenu(self.menuBar)
        self.menufile.setObjectName("menufile")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menufile.menuAction())
        #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#
        #signals
        self.spinBoxTop.valueChanged.connect(self.valuechangeTopY)
        self.spinBoxBottom.valueChanged.connect(self.valuechangeBottomY)
        self.doubleSpinBoxWLLeft.valueChanged.connect(self.valuechangeWLLeft)
        self.doubleSpinBoxWLRight.valueChanged.connect(self.valuechangeWLRight)
        self.spinBoxPointWLRight.valueChanged.connect(self.valuechangePointWLRight)
        self.spinBoxPointWLLeft.valueChanged.connect(self.valuechangePointWLLeft)
        self.pushButtonTakeLeftPoint.clicked.connect(self.CalimPointLeft)
        self.pushButtonTakeRightPoint.clicked.connect(self.CalimPointRight)
        
        self.checkBoxBackGUse.stateChanged.connect(self.backUseChanged)
        self.checkBoxGainBoost.stateChanged.connect(self.gainBoostChanged)
        self.checkBoxStartStop.stateChanged.connect(self.startStopChanged) 
        self.checkBoxTrigger.stateChanged.connect(self.triggerChanged)
        self.checkBoxExposureMax.stateChanged.connect(self.exposureMaxChanged)
        self.checkBoxSpecLog.stateChanged.connect(self.SpecLogChanged)
        self.checkBoxSpecLog1.stateChanged.connect(self.SpecLogChanged1)
        
        self.spinBoxFps.valueChanged.connect(self.valueChangeFps)
        self.spinBoxExposure.valueChanged.connect(self.valueChangeExposure)
        self.spinBoxBoost.valueChanged.connect(self.valueChangeBoost)
        self.spinBoxTriggerDelay.valueChanged.connect(self.valueChangeTriggerDelay)
        self.spinBoxAvgVid.valueChanged.connect(self.valueAvgVid)
        self.spinBoxPixTime.valueChanged.connect(self.valuePixTime)
        self.pushButtonSave.clicked.connect(self.saveSl)
        
        self.spinBoxStageVelocity.valueChanged.connect(self.valueStageVelocity)
        self.pushButtonStagePosSet.clicked.connect(self.StageSetPos)
        self.pushButtonExpStart.clicked.connect(self.expStartSl)
        
        self.checkBoxInit.stateChanged.connect(self.initChanged)
        self.doubleSpinMCP.valueChanged.connect(self.valueChangeMCP)
        self.doubleSpinBoxHRIThr.valueChanged.connect(self.valueChangeHRIThr)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
		
        #restore
        #restore(self.settings)
        #set image
        
        #here is the video
        self.scene = QtWidgets.QGraphicsScene(self.centralWidget)
        
        self.view  = MyGraphicsView(self.scene)
        
        self.widget = QtWidgets.QWidget(self.centralWidget)
        self.widget.setGeometry(QtCore.QRect(20, 2, imageSizeUIx, imageSizeUIy))
        self.layout = QGridLayout() 

        self.widget.setLayout(self.layout)
        self.layout.addWidget(self.view)#, 1, 0)

    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #slots
        self.t1 = time.time()
    @pyqtSlot(QPixmap)
    def setImage(self, pixMap):
        self.scene.clear()
        self.scene.addPixmap(pixMap)

    @pyqtSlot(tuple)
    def setSpectrum(self, spec):
        spectrum = spec[0]
        theorSpectrum = spec[1]
        self.graphicsSpectrum.plot(spectrum[1], spectrum[0], color = 'r',clear=True)
    @pyqtSlot(np.ndarray)
    def setScanPlot(self, scan):
        self.graphicsScan.plot(np.arange(len(scan)), scan, color = 'r',clear=True)

    def SpecLogChanged1(self):
        if self.checkBoxSpecLog1.isChecked():
            self.graphicsSpectrum.setLogMode(y = True)
        else:
            self.graphicsSpectrum.setLogMode(y = False)

    @pyqtSlot(float)
    def changeFpsS(self, fps):
        self.spinBoxFps.setValue(fps)

    @pyqtSlot(float)
    def changeExposureS(self, exposure):
        self.spinBoxExposure.setValue(exposure)

    @pyqtSlot(float)
    def changeBoostS(self, boost):
        self.spinBoxBoost.setValue(boost)   
	
    def CalimPointLeft(self):
        self.takeCalimPointLeft.emit()

    def CalimPointRight(self):
        self.takeCalimPointRight.emit()
		
    def valuechangeTopY(self):
        self.takeTopLevel.emit(self.spinBoxTop.value())
	  
    def valuechangeBottomY(self):
        self.takeBottomLevel.emit(self.spinBoxBottom.value())
		
    def valuechangeWLLeft(self):
        self.takeWVLeft.emit(self.doubleSpinBoxWLLeft.value())
		
    def valuechangeWLRight(self):
        self.takeWVRight.emit(self.doubleSpinBoxWLRight.value())
	
    def valuechangePointWLRight(self):
        self.takePointWVRight.emit(self.spinBoxPointWLRight.value())
	
    def valuechangePointWLLeft(self):
        self.takePointWVLeft.emit(self.spinBoxPointWLLeft.value())
        
    def valueChangeFps(self):
        self.takeFps.emit(self.spinBoxFps.value())
        
    def valueChangeExposure(self):
        self.takeExposure.emit(self.spinBoxExposure.value())

    def valueChangeBoost(self):
        self.takeBoost.emit(self.spinBoxBoost.value())
    
    def valueChangeTriggerDelay(self):
        self.takeTriggerDelay.emit(self.spinBoxTriggerDelay.value())
        
    def valueAvgVid(self):
        self.takeAvgVid.emit(self.spinBoxAvgVid.value())
        
    def valuePixTime(self):
        self.takePixTime.emit(self.spinBoxPixTime.value())
                
    def backUseChanged(self):
        self.backUse.emit(self.checkBoxBackGUse.isChecked())
   
    def gainBoostChanged(self):
        self.gainBoost.emit(self.checkBoxGainBoost.isChecked())
        
    def triggerChanged(self):
        self.trigger.emit(self.checkBoxTrigger.isChecked())
    
    def exposureMaxChanged(self):
        self.exposureMax.emit(self.checkBoxExposureMax.isChecked())
    
    def startStopChanged(self):
        self.startStop.emit(self.checkBoxStartStop.isChecked())
        
    def SpecLogChanged(self):
        self.SpecLog.emit(self.checkBoxSpecLog.isChecked())
        
    def StageSetPos(self):
        self.stageSetPosE.emit(self.spinBoxPosition.value())
        
    def expStartSl(self):
        self.expStartSi.emit((self.spinBoxExpStartPos.value(), self.spinBoxExpStopPos.value()))
    
    def saveSl(self):
        self.saveSi.emit('data')
        
    def valueStageVelocity(self):
        self.takeStageVelocity.emit(self.spinBoxStageVelocity.value())
        
    def initChanged(self):
        self.HRIInit.emit(self.checkBoxInit.isChecked())
        
    def valueChangeMCP(self):
        self.takeMCP.emit(self.doubleSpinMCP.value())
        
    def valueChangeHRIThr(self):
        self.takeHRIThr.emit(self.doubleSpinBoxHRIThr.value())
        
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #names
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Interference"))
        self.groupBox.setTitle(_translate("MainWindow", "area for the cut"))
        self.label.setText(_translate("MainWindow", "y top"))
        self.label_2.setText(_translate("MainWindow", "y bottom"))
        self.label_3.setText(_translate("MainWindow", "x left"))
        self.label_4.setText(_translate("MainWindow", "x right"))
        self.groupBoxCamParam.setTitle(_translate("MainWindow", "parameters of the camera"))
        self.labelStartStop.setText(_translate("MainWindow", "start/stop"))
        self.labelFps.setText(_translate("MainWindow", "fps"))
        self.labelExposure.setText(_translate("MainWindow", "exposure"))
        self.labelExposureMax.setText(_translate("MainWindow", "max exp."))
        self.labelBoost.setText(_translate("MainWindow", "boost"))
        self.labelGainBoost.setText(_translate("MainWindow", "gain_boost"))
        self.labelTrigger.setText(_translate("MainWindow", "ext. trigger"))
        self.labelTriggerDelay.setText(_translate("MainWindow", "delay"))
        self.labelAvgVid.setText(_translate("MainWindow", "avg"))
        self.labelPixTime.setText(_translate("MainWindow", "Pclock"))
        
        self.groupBox_3.setTitle(_translate("MainWindow", "calibration"))
        self.groupBoxSpec.setTitle(_translate("MainWindow", "photo and cut"))        
        self.pushButtonTakeLeftPoint.setText(_translate("MainWindow", "take left point"))
        
        
        
        self.pushButtonTakeRightPoint.setText(_translate("MainWindow", "take right point"))
        self.label_6.setText(_translate("MainWindow", "coordinate"))
        self.label_7.setText(_translate("MainWindow", "coordinate"))
        self.labelLeftPoint.setText(_translate("MainWindow", "value"))
        self.labelRightPoint.setText(_translate("MainWindow", "value"))
        self.menufile.setTitle(_translate("MainWindow", "file"))
        ##P400!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.groupBoxDG.setTitle(_translate("MainWindow", "DG P400"))
        self.labelDGSource.setText(_translate("MainWindow", "source"))
        self.labelDGEdge.setText(_translate("MainWindow", "egdge"))
        self.labelDGTerm.setText(_translate("MainWindow", "term"))
        self.labelDGLvl.setText(_translate("MainWindow", "lvl(V)"))
        self.labelDGGateMode.setText(_translate("MainWindow", "gate mode"))
        self.tabWidgetDG.setTabText(self.tabWidgetDG.indexOf(self.tabTrigger), _translate("MainWindow", "Trigger"))
        self.labelDGAdelay.setText(_translate("MainWindow", "delay"))
        self.labelDGADelayStep.setText(_translate("MainWindow", "delay step"))
        self.labelDGARefCh.setText(_translate("MainWindow", "ref chan"))
        self.labelDGAPol.setText(_translate("MainWindow", "polarity"))
        self.labelDGAVHigh.setText(_translate("MainWindow", "V high"))
        self.labelDGAVLow.setText(_translate("MainWindow", "V low"))
        self.labelDGAWidth.setText(_translate("MainWindow", "width"))
        self.checkBoxDGAOn.setText(_translate("MainWindow", "on/off"))
        self.tabWidgetDG.setTabText(self.tabWidgetDG.indexOf(self.tabChA), _translate("MainWindow", "Channel A"))
        self.checkBoxDGStart.setText(_translate("MainWindow", "start/stop"))
        self.checkBoxDGInit.setText(_translate("MainWindow", "init"))
        ##scan!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.groupBoxScan.setTitle(_translate("iccdApp", "scan"))
        self.pushButtonScanStart.setText(_translate("iccdApp", "scan"))
        self.labelScanStart.setText(_translate("iccdApp", "start"))
        self.labelScanStop.setText(_translate("iccdApp", "stop"))
        self.labelScanStep.setText(_translate("iccdApp", "step"))
        self.pushButtonScanOnPlaceStart.setText(_translate("iccdApp", "start/stop"))
        self.pushButtonScanSave.setText(_translate("iccdApp", "save"))
        
    def closeEvent(self):
        #MainWindow.
        #save(self.settings)
        #QMainWindow.closeEvent(self)
        print("exit event")