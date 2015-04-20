from PyQt4 import QtGui
from PyQt4 import QtCore
 
class ClickableQLabel(QtGui.QLabel):
 
    def __init(self, parent):
        QtGui.QLabel.__init__(self, parent)
        self.unsetCursor()
        self.setCursor(QtCore.Qt.PointingHandCursor)
 
    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))
