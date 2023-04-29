#from CameraClass import Camera
#from pyueye import ueye
from pypylon import pylon
import numpy as np
import cv2
import sys
import time

# is_SetExternalTrigger (HIDS hf, INT nTriggerMode)
#IS_SET_TRIG_LO_HI
#IS_SET_TRIG_OFF
# is_SetTriggerDelay (HIDS hf, INT nDelay)


class camWork():
    def __init__(self, camNum = 0):
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()
        for device in devices:
            print(device.GetFriendlyName())
        if devices == []:
            print('there is no camera found. Dude look for it better')

        else:
            self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            self.camera.Open()
            print(self.camera.GetSfncVersion)
            print('model',self.camera.DeviceModelName.GetValue(), 
                ';serialNum', self.camera.DeviceSerialNumber.GetValue(),
                ';manufacturer', self.camera.DeviceManufacturerInfo.GetValue(),
                ';VendorName', self.camera.DeviceVendorName.GetValue(),
                ';sensor size', self.camera.SensorWidth.GetValue(), 'x', self.camera.SensorHeight.GetValue(),
                ';temperature', self.camera.DeviceTemperature.GetValue())
            self.camera.PixelFormat.SetValue('Mono8')
    def __exit__(self, _type, value, traceback):
        self.Exit()

    def Exit(self):
        if self.camera.IsGrabbing():
            self.camera.StopGrabbing()
        if self.camera.AcquisitionStatus.GetValue():
            self.camera.AcquisitionStop.Execute()
        self.camera.Close()
        print('camera disconnected')
    #def triggerMode(self, ):
    
    #def continuousMode(self, ):
    def GetExposureRange(self):
        #values=ueye.IS_RANGE_F64()
        #ueye.is_Exposure(self.hCam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE, values, ueye.sizeof(values))        
        #return values.f64Min.value,values.f64Max.value, values.f64Inc.value
        pass
        
    def getExposureMax(self):
        return self.camera.ExposureTime.GetMax()
   
    def setExposureMax(self):
        return self.camera.ExposureTime.SetValue(self.camera.ExposureTime.GetMax())
        
    def freezeVIdeo(self, onOff):
        if onOff:
            self.camera.AcquisitionStop.Execute()
        else:
            self.camera.AcquisitionStart.Execute()

    def stopVIdeo(self):
        if self.camera.IsGrabbing():
            self.camera.StopGrabbing()
        if self.camera.AcquisitionStatus.GetValue():
            self.camera.AcquisitionStop.Execute()
                
    def setGainBoost(self, onOff):
        print('no gain boost for this cam')
        #if onOff:
        #    return ueye.is_SetGainBoost(self.hCam, ueye.IS_SET_GAINBOOST_ON)
        #if not onOff:
        #    return ueye.is_SetGainBoost(self.hCam, ueye.IS_SET_GAINBOOST_OFF)
    
    def setExternalTrigger(self, onOff):
        # if onOff:
            # if self.camera.IsGrabbing():
                # self.camera.StopGrabbing()
            # if self.camera.AcquisitionStatus.GetValue():
                # self.camera.AcquisitionStop.Execute()
            # self.camera.AcquisitionMode.SetValue('Continuous')
            # self.camera.TriggerSelector.SetValue('FrameStart')
            # self.camera.TriggerMode.SetValue('On');
            # self.camera.TriggerActivation.SetValue('RisingEdge');
            # self.camera.ExposureMode.SetValue('Timed');
            # self.camera.AcquisitionStart.Execute()
            # self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
            
        # if not onOff:
            # if self.camera.IsGrabbing():
                # self.camera.StopGrabbing()
            # if self.camera.AcquisitionStatus.GetValue():
                # self.camera.AcquisitionStop.Execute()
            # self.camera.AcquisitionMode.SetValue('Continuous')
            # self.camera.TriggerSelector.SetValue('FrameStart')
            # self.camera.TriggerMode.SetValue('Off')
            # self.camera.AcquisitionStart.Execute()
            # self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        if onOff:
            self.camera.TriggerMode.SetValue('On')
            self.camera.TriggerActivation.SetValue('RisingEdge')
        else:
            self.camera.TriggerMode.SetValue('Off')
            
    def setTriggerDelay(self, delay):
        return self.camera.TriggerDelay.SetValue(delay)
    
    def SetGain(self,gain):
        return self.camera.Gain.SetValue(gain)
        
    def SetExposure(self, time):
        return self.camera.ExposureTime.SetValue(time)

    def SetFramerate(self, fps): 
        return self.camera.AcquisitionFrameRate.SetValue(fps)

    def SetPixelclock(self, clock):
        print('no pix clock for this cam')
        #clock=ueye.uint(clock)
        #return ueye.is_PixelClock(self.hCam, ueye.IS_PIXELCLOCK_CMD_SET, clock, ueye.sizeof(clock))
    
    def GetGain(self):
        return self.camera.Gain.GetValue()
        
    def GetExposure(self):
        return self.camera.ExposureTime.GetValue()
        
    def GetFramerate(self):
        return self.camera.AcquisitionFrameRate.GetValue()

    def GetPixelclock(self):
        return 0
        
    def captureVideo(self):
        self.camera.AcquisitionStart.Execute( )
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed 
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    def takeImage(self):
        if self.camera.IsGrabbing(): 
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                image = self.converter.Convert(grabResult)
                img = image.GetArray()
                return img
        else:
            self.camera.StopGrabbing()
            self.camera.AcquisitionStop.Execute( )
            print('could not take a pic')
            return np.zeros([1200, 1920])