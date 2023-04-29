import numpy as np 
import os, sys

from PyQt5.QtWidgets import QGraphicsView, QWidget
from PyQt5.QtCore import pyqtSignal, QPoint, QPointF, Qt

class MyGraphicsView(QGraphicsView):
    cursorPosChanged = pyqtSignal()
    dragged = pyqtSignal(QPoint)
    draggingStopped = pyqtSignal()
    scrolled = pyqtSignal(bool)
    scaleChanged = pyqtSignal(int, int)

    def __init__(self, parent):
        super(MyGraphicsView, self).__init__(parent)

        self.setMouseTracking(True)
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)

        self.currentScaleFactor = 1
        self.defaultScaleFactor = 1.1
        self.max_zoom = 20
        self.cursorPos = QPointF(0, 0)
        self.scrollPos = QPointF(0, 0)
        self.clickPos = np.array([QPointF(-1, -1), QPointF(-1, -1), QPointF(-1, -1)])
        self.isScrolling = False

    def getCursorPos(self):
        return self.cursorPos

    def wheelEvent(self, e):
        # Change colorscale of BEC Image when Ctrl/Shift is pressed while scrolling
        # if e.modifiers().testFlag(Qt.ControlModifier): # Higher limit
        #     self.scaleChanged.emit(1, e.angleDelta.y < 0)
        #     return 
        # elif e.modifiers().testFlag(Qt.ShiftModifier): # lower limit
        #     self.scaleChanged.emit(-1, e.angleDelta.y < 0)
        #     return

        scaleFactor = self.defaultScaleFactor
        if(e.angleDelta().y() > 0):                         # zoom in
            self.scrolled.emit(True)
            if(self.currentScaleFactor > self.max_zoom): return
            if(self.currentScaleFactor * scaleFactor > self.max_zoom):
                scaleFactor = self.max_zoom / self.currentScaleFactor
            
            self.scale(scaleFactor, scaleFactor)
            self.currentScaleFactor *= scaleFactor
        else:                                           # zoom out
            self.scrolled.emit(False)
            if self.currentScaleFactor < scaleFactor:
                scaleFactor = self.currentScaleFactor
            
            self.scale(1/scaleFactor, 1/scaleFactor)
            self.currentScaleFactor /= scaleFactor
        
    def mouseMoveEvent(self, e):
        if self.isScrolling:
            tmp = e.pos() - self.scrollPos
            dxdy = QPoint(int(tmp.x()), int(tmp.y()))
            # Come on, there has to be a cooler way...
            # I don't even understand why exactly this works... what is the scrollbar value actually representing?
            # But it's actually a nice way since calling the sliders automatically protects you against undefined behavior
            self.horizontalScrollBar().setSliderPosition(self.horizontalScrollBar().value() - dxdy.x())
            self.verticalScrollBar().setSliderPosition(self.verticalScrollBar().value() - dxdy.y())
            self.scrollPos = e.pos()
            self.dragged.emit(dxdy)
        
        self.cursorPos = self.mapToScene(e.pos())
        self.cursorPosChanged.emit()

    def scrollLeftRight(self, dx):
        self.horizontalScrollBar().setSliderPosition(self.horizontalScrollBar().value() + dx)

    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            self.scrollPos = e.pos()
            self.isScrolling = True
        # elif (e.buttons() == Qt.RightButton and e.modifiers.testFlag(Qt.ShiftModifier)):
        #     self.clickPos[2] = self.mapToScene(e.pos())
        # elif (e.buttons() == Qt.RightButton and e.modifiers.testFlag(Qt.ControlModifier)):
        #     self.clickPos[1] = self.mapToScene(e.pos())
        elif (e.buttons() == Qt.RightButton):
            self.clickPos[0] = self.mapToScene(e.pos())
        elif (e.buttons() == Qt.MiddleButton):
            self.scaleChanged.emit(0, 0) # causes autoscale
        
        self.cursorPosChanged.emit()

    def mouseReleaseEvent(self, e):
        # The widget that received the MousePressEvent will also receive the corresponding MouseReleaseEvent
        self.isScrolling = False
        self.draggingStopped.emit()


    def getClickPos(self, i):
        if (i < self.clickPos.size()): 
            return self.clickPos[i] 
        else: 
            return QPointF(0, 0)

    def getClickPosInt(self, i):
        if (i < self.clickPos.size()): 
            return int(self.clickPos[i]) 
        else: 
            return QPoint(0, 0)
