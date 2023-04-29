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


def readSpec(specName, delimiter):
    x = np.array([])
    y = np.array([])
    with open(specName, newline='') as f:
        fr = csv.reader(f, delimiter=delimiter, quotechar='|')
        for row in fr:
            if row != []:
                y = np.append(y, float(row[0]))
                x = np.append(x, float(row[1]))
                
    #x = x.astype(np.float)
    #y = y.astype(np.float)
    return y, x
tx, ty = readSpec('transmission_losgatos.dat', ' ')    

def func(x, a, b, c, d, e, f):
     return (a + b * x + c * x ** 2 + d * x ** 3 + e * x ** 4 + f * x ** 5)
     
def transM(y, x, ty, tx):
    xmin = min(np.where(tx >= (min(x)))[0])
    xmax = max(np.where(tx <= (max(x)))[0])
    xmax = max(np.where(tx <= (max(x)))[0])
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
  
def calcArrScan(arrScan, arr):
    arrSum = np.average(arr)
    return np.append(arrScan, arrSum)
    
def checkFolderExp(direct = 'data/exp'):
    ii = 0
    folder = '666'
    while ii < 6666:
        ii += 1
        folder = direct + str(ii)
        if not os.path.exists(folder):
            ii = 6668
    return(folder)
    
def specFit(x, y, step = 3, phDiff = 1000):
    print(x)
    xdown = np.where(x >= 555)[0][-1]
    xtop = np.where(x < 590)[0][0]
    x1 = x[xtop:xdown]
    y1 = y[xtop:xdown]
    Lc = x1[np.argmax(y1)]     
    xdown = np.where(x1 >= Lc-5)[0][-1]
    xtop = np.where(x1 < Lc+1.5)[0][0]
    xc = x1[xtop:xdown]
    yc = y1[xtop:xdown]
    
    phNumT = 150000
    phNumD = 80000
    ii = 0
    phNumL = np.arange(80000, 150000, 2500)
    LcL = np.arange(568,574, 1)
    while phNumT -  phNumD > phDiff and ii < 20:
        ii += 1
        thT = specFromFile(phNumT, phNumL, Lc, LcL)
        
        thT = cutspec(thT[0], thT[1], down = Lc+1.5, top = Lc - 5)
        diffT = np.sum(calcDiff(xc, yc, thT[0], thT[1]))
        
        thD = specFromFile(phNumD, phNumL, Lc, LcL)    
        thD = cutspec(thD[0], thD[1], down = Lc+1.5, top = Lc - 5)
        diffD = np.sum(calcDiff(xc, yc, thD[0], thD[1]))
        if diffT*diffD < 0:
            if abs(diffT) < abs(diffD):
                m1 = abs(1/diffD)
                m2 = abs(1/diffT)
                dist = m2/(m1+m2) * (phNumT - phNumD)/step
                phNumD += abs(max(dist,2000))
            else:
                m1 = abs(1/diffT)
                m2 = abs(1/diffD)
                dist = m2/(m1+m2) * (phNumT - phNumD)/step
                phNumT -= abs(max(dist, 2000))
        else:
            if diffT < 0:
                phNumD -= 10000
            else:
                phNumT += 10000
        
        #print('top', phNumT, '\n down', phNumD, '\n diff top', diffT, '\n diff down', diffD)
    #print(ii)
    return (phNumT + phNumD)/2
    
def convolution(num, wl, cWidth = 300):
    convNum = np.arange(-50, 51, 1)
    addZ = 500
    numC = np.zeros(len(num) + addZ * 2)
    num = np.append(np.zeros(addZ) , np.append(num, np.zeros(addZ)))
    
    wlStep = abs(wl[-1] - wl[-2])
    wlC1 = np.arange(min(wl), min(wl) - wlStep * addZ,-wlStep)
    
    wlStep = abs(wl[1] - wl[0])
    wlC2 = np.arange(max(wl) + wlStep * addZ, max(wl),-wlStep)
    
    wlC = np.append(wlC2, np.append(wl, wlC1))
    
    ii = -1
    
    for wl1 in wlC:
        ii += 1
        for jj in convNum:
            if jj + ii > 0 and jj + ii < len(numC):
                numC[ii + jj] += num[ii] * np.sqrt(1/ (np.pi * cWidth)) * np.exp(-jj ** 2 / cWidth)
    return numC, wlC    