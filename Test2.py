from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QPixmap
import sys

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Przykład PyQt')
        self.setGeometry(600, 100, 800, 800)

        self.button = QPushButton('Kliknij mnie', self)
        self.button.setGeometry(580, 40, 150, 40)
        self.button.clicked.connect(self.updateCanvas)

        self.line1 = QLineEdit(self)
        self.line1.setGeometry(20, 40, 100, 40)

        self.line2 = QLineEdit(self)
        self.line2.setGeometry(160, 40, 100, 40)

        self.line3 = QLineEdit(self)
        self.line3.setGeometry(300, 40, 100, 40)

        self.line4 = QLineEdit(self)
        self.line4.setGeometry(440, 40, 100, 40)

        self.modified = True
        self.pm = QPixmap()
        self.func = None

        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

    def paintEvent(self, event):
        if self.modified:
            pixmap = QPixmap(540, 400)
            pixmap.fill(Qt.white)

            painter = QPainter(pixmap)
            self.drawBackground(painter)
            self.pm = pixmap

        qp = QPainter(self)
        qp.drawPixmap(20, 140, self.pm)

    def drawBackground(self, qp):
        func = self.func
        if func is not None:
            self.func(qp)

    def drawBlock(self, qp):

        try:
            self.x1 = float(self.line1.text())
            self.y1 = float(self.line2.text())
            self.x2 = float(self.line3.text())
            self.y2 = float(self.line4.text())
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Invalid input. Please enter numeric values only.')
            return

        pixmap = QPixmap(540, 400)
        pixmap.fill(Qt.white)

        painter = QPainter(pixmap)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)
        qp.drawPixmap(20, 140, pixmap)

    def updateCanvas(self):
        self.func = self.drawBlock
        self.modified = True
        self.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
