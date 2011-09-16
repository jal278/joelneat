#!/usr/bin/python

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import hyperneat
import random

object_hash = dict()

class Artist(QtGui.QWidget):
    def render_image(self,p,scale):
        size=len(p)*scale
       	img = QtGui.QImage(len(p)*scale,len(p)*scale,QtGui.QImage.Format_RGB32)
        for x in xrange(len(p)):
         for y in xrange(len(p)):
          v=abs(int(p[y][x]*255.0)) << 16
          for xx in xrange(scale):
           for yy in xrange(scale):
            img.setPixel(x*scale+xx,y*scale+yy,v)
        return img,size

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.RightButton:
            return

        itemData = QtCore.QByteArray()
        mimeData = QtCore.QMimeData()
        dataStream = QtCore.QDataStream(itemData,QtCore.QIODevice.WriteOnly)
        print self.uuid
        dataStream << QtCore.QString(self.uuid)
        drag = QtGui.QDrag(self)
        drag.setHotSpot(e.pos() - self.pos())
        mimeData.setData('application/blah',itemData)
        drag.setMimeData(mimeData)
        dropAction = drag.start(QtCore.Qt.MoveAction)
    def __init__(self,art,parent):
        self.uuid=str(random.random())
        object_hash[self.uuid]=self
        art.render_picture()
        self.pic=art.get_picture()

        super(Artist, self).__init__(parent)

        self.initUI()
        
    def initUI(self):

        self.setAcceptDrops(True)
        self.image,self.size = self.render_image(self.pic,3)
        self.resize(self.size, self.size)
    def paintEvent(self,event):
        painter=QtGui.QPainter(self)
        painter.drawImage(0,0,self.image)

class Interactive(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAcceptDrops(True)

        for k in range(4):
         a=hyperneat.artist()
         artist=Artist(a,self)
         artist.move(k*100,0)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        print "drop event"
        position = e.pos()
        if(e.mimeData().hasFormat('application/blah')):
           itemData=e.mimeData().data('application/blah')
           dataStream = QtCore.QDataStream(itemData,QtCore.QIODevice.ReadOnly)
           uuid=QtCore.QString()
           dataStream >> uuid
           obj=object_hash[str(uuid)]
           obj.move(e.pos())
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAcceptDrops(True)

        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Tetris')
	self.interactive = Interactive(self)

	self.setCentralWidget(self.interactive)

	self.statusbar = self.statusBar()
	self.connect(self.interactive, QtCore.SIGNAL("messageToStatusbar(QString)"), 
	    self.statusbar, QtCore.SLOT("showMessage(QString)"))

        self.center()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, 
	    (screen.height()-size.height())/2)

def main():

  
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec_()  


if __name__ == '__main__':
    main()

