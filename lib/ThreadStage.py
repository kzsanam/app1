from PyQt5.QtCore import *
import time

class ThreadStage(QThread):
    #signals
    stagePosS = pyqtSignal(str)
    
    #print(motor.is_in_motion, type(motor.is_in_motion))
    def initStageSl(self, init):
        if init:
            #self.stagePos = 0.0
            #sorry import is here, just this lib from thorlabs is working very strange. takes a lot to downoload and doesn't work if stage was not connected when it started.
            import thorlabs_apt as apt
            devList = apt.list_available_devices()
            print('available devices from thorlabs', devList, 'stage info',apt.hardware_info(devList[0][1]))
            dev1 = devList[0][1]
            self.motor = apt.Motor(dev1)
    #motor.serial_number
    #motor.is_in_motion
            velParLimt = self.motor.get_velocity_parameter_limits()
            print('velocity limits', velParLimt)
            velPar = self.motor.get_velocity_parameters() #min vel, acc, max vel
            print('min vel, acc, max vel',velPar)
    
            self.motor.set_velocity_parameters(velPar[0], velPar[1], velPar[2])
    
            velPar = self.motor.get_velocity_parameters() #min vel, acc, max vel
            print('min vel, acc, max vel',velPar)
    #motor.get_velocity_parameter_limits() #max acc, max vel
    #motor.get_move_home_parameters() #(direction, limiting switch, velocity, zero offset)
    #motor.get_stage_axis_info()
    #motor.is_in_motion()
            self.stageSetPosBool = False
            self.stageHomeBool = False
            self.setPos = 0
            self.velocity = float()
            self.stagePosS.emit(str(self.motor.position))
        else:
            self.motor.disable()
            
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
        #self.initStageSl()
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