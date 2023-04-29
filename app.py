import sys
import qdarkstyle
from PyQt5 import  QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from mainwindow import Ui_MainWindow
from windowSpec import Ui_WindowSpec

from lib.HRIQT import HRI
from lib.DGComQT import DGComQT
from lib.ThreadExp import ThreadExp
from lib.ThreadStage import ThreadStage
from lib.ThreadCam import ThreadCam
from lib.ThreadSpec import ThreadSpec

def main():
    app = QtWidgets.QApplication(sys.argv )
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    #main win
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #spec win
    windowSpec = QWidget()
    ui2 = Ui_WindowSpec()
    ui2.setupUi(windowSpec)
    windowSpec.show()
    
    app.aboutToQuit.connect(ui.closeEvent)
    #app.aboutToQuit.connect(ThreadStage.closeEvent)
    #interferometer camera
    th = ThreadCam()
    th.changePixmap.connect(ui.setImage)
    th.changePixmap2.connect(ui.setSpectrum)
    th.changeScanPlot.connect(ui.setScanPlot)
    
    ui.takeTopLevel.connect(th.takeTopLevelS)
    ui.takeBottomLevel.connect(th.takeBottomLevelS)
    ui.spinBoxLeft.valueChanged.connect(th.boxLeftSl)
    ui.spinBoxRight.valueChanged.connect(th.boxRightSl)
 
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
    ui.checkBoxImQual.stateChanged.connect(th.changeImQual)
    
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
    
    ui.pushButtonScanOnPlaceStart.clicked.connect(th.ScanOnPlaceStart)
    ui.pushButtonScanStart.clicked.connect(th.ScanStartSl)
    ui.pushButtonScanSave.clicked.connect(th.scanSave)
    #th.changeScanPos.connect(ui.doubleSpinBoxDGAdelay)
    #ui.pushButtonScanStart
    
    ui.checkBoxInitCam.stateChanged.connect(th.start)
    ui.checkBoxInitCam.stateChanged.connect(th.initCam)    
    th.changeFps.connect(ui.spinBoxFps.setValue)
    th.changeExposure.connect(ui.spinBoxExposure.setValue)
    th.changeBoost.connect(ui.spinBoxBoost.setValue)
    th.changePixTime.connect(ui.spinBoxPixTime.setValue)
    
    th.getCenterL.connect(ui.spinBoxPointWLLeft.setValue)
    th.getCenterR.connect(ui.spinBoxPointWLRight.setValue)
    #th..connect(ui.checkBoxGainBoost.isChecked)
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #stage
    thStage = ThreadStage()
    ui.checkBoxInitStage.clicked.connect(thStage.initStageSl)
    thStage.stagePosS.connect(ui.labelPositionShow.setText)
    ui.stageSetPosE.connect(thStage.stageSetPosS)
    ui.takeStageVelocity.connect(thStage.stageSetVelocityS)
    ui.pushButtonStageHome.clicked.connect(thStage.stageHome)
    
    #thStage.stagePosS.emit(str(thStage.motor.position))
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
    ui.spinBoxTop.setValue(0)
    ui.spinBoxBottom.setValue(300)
    ui.doubleSpinBoxWLLeft.setValue(0)
    ui.doubleSpinBoxWLRight.setValue(20)
    ui.spinBoxPointWLRight.setValue(0)
    ui.spinBoxPointWLLeft.setValue(1)
    ui.spinBoxLeft.setValue(1)
    ui.spinBoxRight.setValue(100)
    
########################################################################
#spec is here
    thSpec = ThreadSpec()
    thSpec.changePixmap.connect(ui2.setImage)
    thSpec.changePixmap2.connect(ui2.setSpectrum)
    #thSpec.start()
    ui2.checkBoxInitCam.stateChanged.connect(thSpec.start)
    ui2.takeTopLevel.connect(thSpec.takeTopLevelS)
    ui2.takeBottomLevel.connect(thSpec.takeBottomLevelS)
    ui2.takeWVLeft.connect(thSpec.takeWVLeftS)
    ui2.takeWVRight.connect(thSpec.takeWVRightS)
    ui2.takePointWVLeft.connect(thSpec.takepointWVLeftS)
    ui2.takePointWVRight.connect(thSpec.takepointWVRightS)
    ui2.takeCalimPointLeft.connect(thSpec.takeCalimPointLeftS)
    ui2.takeCalimPointRight.connect(thSpec.takeCalimPointRightS)
    ui2.takeFps.connect(thSpec.takeFpsS)
    ui2.takeExposure.connect(thSpec.takeExposureS)
    ui2.takeBoost.connect(thSpec.takeBoostS)
    ui2.takeTriggerDelay.connect(thSpec.takeTriggerDelayS)
    ui2.takeAvgVid.connect(thSpec.takeAvgVidS)
    ui2.pushButtonSave.clicked.connect(thSpec.saveS)
    ui2.pushButtonBackTake.clicked.connect(thSpec.backTakeS)
    ui2.backUse.connect(thSpec.backUseS)
    ui2.gainBoost.connect(thSpec.gainBoostS)
    ui2.trigger.connect(thSpec.triggerS)
    ui2.startStop.connect(thSpec.startStopS)
    ui2.exposureMax.connect(thSpec.exposureMaxS)
    
    ui2.SpecLog.connect(thSpec.SpecLogS)
    thSpec.changeFps.connect(ui2.spinBoxFps.setValue)
    thSpec.changeExposure.connect(ui2.spinBoxExposure.setValue)
    thSpec.changeBoost.connect(ui2.spinBoxBoost.setValue)
    
    thSpec.getCenterL.connect(ui2.spinBoxPointWLLeft.setValue)
    thSpec.getCenterR.connect(ui2.spinBoxPointWLRight.setValue)
    thSpec.findPhNum.connect(ui2.labelPhotonNumberValue.setText)
    #th..connect(ui.checkBoxGainBoost.isChecked)
    
    #thSpec.start()
    
    #set values
    ui2.spinBoxTop.setValue(700)
    ui2.spinBoxBottom.setValue(300)
    
    ui2.doubleSpinBoxWLLeft.setValue(568.85)
    ui2.doubleSpinBoxWLRight.setValue(571.08)
    ui2.spinBoxPointWLLeft.setValue(553)
    ui2.spinBoxPointWLRight.setValue(529)
    sys.exit( app.exec_() )
if __name__ == "__main__":
    main()