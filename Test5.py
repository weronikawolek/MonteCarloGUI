from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QPixmap
import sys

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyQt')
        self.setGeometry(600, 100, 800, 800)

        self.button = QPushButton('Kliknij mnie', self)
        self.button.setGeometry(580, 40, 150, 40)
        self.button.clicked.connect(self.update)

        self.lx1 = QLineEdit(self)
        self.lx1.setGeometry(20, 40, 100, 40)

        self.ly1 = QLineEdit(self)
        self.ly1.setGeometry(160, 40, 100, 40)

        self.lx2 = QLineEdit(self)
        self.lx2.setGeometry(300, 40, 100, 40)

        self.ly2 = QLineEdit(self)
        self.ly2.setGeometry(440, 40, 100, 40)

        self.modified = True
        self.pm = QPixmap()
        self.func = None, None

        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

    def paintEvent(self, event):
        if self.modified:
            pixmap = QPixmap(520, 400)
            pixmap.fill(Qt.white)

            painter = QPainter(pixmap)
            self.drawBackground(painter)
            self.pm = pixmap

        qp = QPainter(self)
        qp.drawPixmap(20, 140, self.pm)

    def drawBackground(self, qp):
        func, kwargs = self.func
        if func is not None:
            kwargs["qp"] = qp
            func(**kwargs)

    def drawBlock(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)

        qp.setPen(pen)
        qp.drawRect(self.x1,self.y1, self.x2, self.y2)

    def update(self):
        try:
            self.tx1 = 10*float(self.lx1.text())
            self.ty1 = 10*float(self.ly1.text())
            self.tx2 = 10*float(self.lx2.text())
            self.ty2 = 10*float(self.ly2.text())

            self.x1 = int(self.tx1)
            self.y1 = int(self.ty1)
            self.x2 = int(self.tx2)
            self.y2 = int(self.ty1)

        except ValueError:
            QMessageBox.critical(self, 'Error', 'Invalid input. Please enter numeric values only.')
            return

        self.func = (self.drawBlock, {})
        self.modified = True
        self.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
