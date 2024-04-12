from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QFont, QPen, QColor, QPixmap
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.mModified = True
        self.initUI()
        self.currentRegion = QRect(200, 200, 400, 400)

        self.mPixmap = QPixmap()
        self.func = (None, None)

    def initUI(self):
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Painter training')
        self.show()

    def paintEvent(self, event):
        if self.mModified:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.white)
            painter = QPainter(pixmap)
            painter.drawPixmap(0, 0, self.mPixmap)
            self.drawBackground(painter)
            self.mPixmap = pixmap
            self.mModified = False

        qp = QPainter(self)
        qp.drawPixmap(0, 0, self.mPixmap)

    def drawBackground(self, qp):
        func, kwargs = self.func
        if func is not None:
            kwargs["qp"] = qp
            func(**kwargs)

    def drawFundBlock(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        pen.setStyle(Qt.DashLine)

        qp.setPen(pen)
        qp.drawLine(self.x, self.y)

    def drawNumber(self, qp, notePoint):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(QFont('Arial', 10))
        qp.drawText(notePoint, "5")

    def nextRegion(self):
        self.x0 += 30
        self.x1 += 30
        self.y0 += 30
        self.y1 += 30

    def keyPressEvent(self, event):
        gey = event.key()
        self.func = (None, None)
        if gey == Qt.Key_M:
            print("Key 'm' pressed!")
        elif gey == Qt.Key_Right:
            print("Right key pressed!, call drawFundBlock()")
            self.func = (self.drawFundBlock, {})
            self.mModified = True
            self.update()
            self.nextRegion()
        elif gey == Qt.Key_5:
            print("#5 pressed, call drawNumber()")
            self.func = (self.drawNumber, {"notePoint": QPoint(100, 100)})
            self.mModified = True
            self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())