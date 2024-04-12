from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PIL import ImageTk, Image
import time
from subprocess import Popen, PIPE
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage import gaussian_filter
import PIL.Image
import csv
import sys
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setGeometry(0, 45, 1920, 1080)
        self.setWindowTitle('Monte Carlo Simulation')
        self.setStyleSheet('background-color: lavenderblush;')

        self.titleFont = QFont('Harlow Solid Italic', 25, True)
        self.regularFont = QFont('Ebrima', 12, True)
        self.smallFont = QFont('Ebrima', 10, True)
        self.lineFont = QFont('Ebrima', 8, True)

        self.modified = True
        self.pm = QPixmap()
        self.func = None, None

        self.initUI()

    def initUI(self):
        titleLb = QLabel('Monte-Carlo modeling of optical sensors for postoperative free flap monitoring', self)
        titleLb.setFont(self.titleFont)
        titleLb.setStyleSheet('color: palevioletred;')
        titleLb.setGeometry(200, 0, 2000, 80)

        lb1 = QLabel('1. Choose wavelength from 300 to 1000 [nm]:', self)
        lb1.setFont(self.regularFont)
        lb1.setGeometry(60, 90, 500, 40)

        self.q1 = QLineEdit(self)
        self.q1.setFont(self.lineFont)
        self.q1.setMaxLength(4)
        self.q1.setTextMargins(60, 2, 60, 2)
        self.q1.setFrame(True)
        self.q1.setGeometry(60, 130, 180, 30)

        lb2 = QLabel('2. Choose tissue parameters:', self)
        lb2.setFont(self.regularFont)
        lb2.setGeometry(60, 180, 500, 40)

        lbDermis = QLabel('• Dermis [1-5 mm]', self)
        lbDermis.setFont(self.smallFont)
        lbDermis.setGeometry(60, 220, 200, 30)

        self.qDermis = QLineEdit(self)
        self.qDermis.setFont(self.lineFont)
        self.qDermis.setMaxLength(4)
        self.qDermis.setTextMargins(32, 2, 32, 2)
        self.qDermis.setFrame(True)
        self.qDermis.setGeometry(60, 250, 100, 30)

        lbFat = QLabel('• Fat [1-15 mm]', self)
        lbFat.setFont(self.smallFont)
        lbFat.setGeometry(280, 220, 200, 30)

        self.qFat = QLineEdit(self)
        self.qFat.setFont(self.lineFont)
        self.qFat.setMaxLength(4)
        self.qFat.setTextMargins(32, 2, 32, 2)
        self.qFat.setFrame(True)
        self.qFat.setGeometry(280, 250, 100, 30)

        lbMuscle = QLabel('• Muscle [1-20 mm]', self)
        lbMuscle.setFont(self.smallFont)
        lbMuscle.setGeometry(500, 220, 200, 30)

        self.qMuscle = QLineEdit(self)
        self.qMuscle.setFont(self.lineFont)
        self.qMuscle.setMaxLength(4)
        self.qMuscle.setTextMargins(32, 2, 32, 2)
        self.qMuscle.setFrame(True)
        self.qMuscle.setGeometry(500, 250, 100, 30)

        lbDistance = QLabel('• Distance [1-10 mm]', self)
        lbDistance.setFont(self.smallFont)
        lbDistance.setGeometry(60, 300, 200, 30)

        self.qDistance = QLineEdit(self)
        self.qDistance.setFont(self.lineFont)
        self.qDistance.setMaxLength(4)
        self.qDistance.setTextMargins(32, 2, 32, 2)
        self.qDistance.setFrame(True)
        self.qDistance.setGeometry(60, 330, 100, 30)

        lbLength = QLabel('• Length [1-10 mm]', self)
        lbLength.setFont(self.smallFont)
        lbLength.setGeometry(280, 300, 200, 30)

        self.qLength = QLineEdit(self)
        self.qLength.setFont(self.lineFont)
        self.qLength.setMaxLength(4)
        self.qLength.setTextMargins(32, 2, 32, 2)
        self.qLength.setFrame(True)
        self.qLength.setGeometry(280, 330, 100, 30)

        lbWidth = QLabel('• Width [1-10 mm]', self)
        lbWidth.setFont(self.smallFont)
        lbWidth.setGeometry(500, 300, 200, 30)

        self.qWidth = QLineEdit(self)
        self.qWidth.setFont(self.lineFont)
        self.qWidth.setMaxLength(4)
        self.qWidth.setTextMargins(32, 2, 32, 2)
        self.qWidth.setFrame(True)
        self.qWidth.setGeometry(500, 330, 100, 30)

        lb3 = QLabel('3. Tissue representation:', self)
        lb3.setFont(self.regularFont)
        lb3.setGeometry(60, 380, 500, 40)

        lb4 = QLabel('4. Choose simulation parameters:', self)
        lb4.setFont(self.regularFont)
        lb4.setGeometry(60, 850, 500, 40)

        lbPhotons = QLabel('• Number of photons:', self)
        lbPhotons.setFont(self.smallFont)
        lbPhotons.setGeometry(60, 890, 400, 30)

        self.qPhotons = QLineEdit(self)
        self.qPhotons.setFont(self.lineFont)
        self.qPhotons.setMaxLength(4)
        self.qPhotons.setTextMargins(32, 2, 32, 2)
        self.qPhotons.setFrame(True)
        self.qPhotons.setGeometry(60, 920, 100, 30)

        lbAnizo = QLabel('• Anisotropy [-0.9 - 0.9]:', self)
        lbAnizo.setFont(self.smallFont)
        lbAnizo.setGeometry(300, 890, 400, 30)

        self.qAnizo = QLineEdit(self)
        self.qAnizo.setFont(self.lineFont)
        self.qAnizo.setMaxLength(4)
        self.qAnizo.setTextMargins(32, 2, 32, 2)
        self.qAnizo.setFrame(True)
        self.qAnizo.setGeometry(300, 920, 100, 30)

        lbIndex = QLabel('• Index of refraction medium [1.1 - 20]:', self)
        lbIndex.setFont(self.smallFont)
        lbIndex.setGeometry(540, 890, 400, 30)

        self.qIndex = QLineEdit(self)
        self.qIndex.setFont(self.lineFont)
        self.qIndex.setMaxLength(4)
        self.qIndex.setTextMargins(32, 2, 32, 2)
        self.qIndex.setFrame(True)
        self.qIndex.setGeometry(540, 920, 100, 30)

        self.btnDraw = QPushButton('Draw tissue representation', self)
        self.btnDraw.setStyleSheet('background-color: pink; color: black;')
        self.btnDraw.setFont(self.smallFont)
        self.btnDraw.setGeometry(1000, 150, 360, 50)
        self.btnDraw.clicked.connect(self.update)

        self.btnSave = QPushButton('Save the data to the file', self)
        self.btnSave.setStyleSheet('background-color: pink; color: black;')
        self.btnSave.setFont(self.smallFont)
        self.btnSave.setGeometry(1000, 230, 360, 50)

        self.btnFile = QPushButton('Choose the file', self)
        self.btnFile.setStyleSheet('background-color: pink; color: black;')
        self.btnFile.setFont(self.smallFont)
        self.btnFile.setGeometry(1490, 150, 360, 50)

        self.btnSim = QPushButton('Start simulation', self)
        self.btnSim.setStyleSheet('background-color: pink; color: black;')
        self.btnSim.setFont(self.smallFont)
        self.btnSim.setGeometry(1490, 230, 360, 50)

    def paintEvent(self, event):
        if self.modified:
            pixmap = QPixmap(600, 400)
            pixmap.fill(Qt.white)

            painter = QPainter(pixmap)
            self.drawBackground(painter)
            self.pm = pixmap

        qp = QPainter(self)
        qp.drawPixmap(60, 430, self.pm)

    def drawBackground(self, qp):
        func, kwargs = self.func
        if func is not None:
            kwargs["qp"] = qp
            func(**kwargs)

    def drawTissue(self, qp):

        qp.fillRect(100, 100, 400, self.z1, QColor(247, 231, 210))
        qp.fillRect(100, 100 + self.z1, 400, (self.z1 + self.z2), QColor(242, 224, 145))
        qp.fillRect(100, 100 + (self.z1 + self.z2), 400, (self.z1 + self.z2 + self.z3), QColor(237, 202, 223))
        qp.fillRect(120, 100, 45, 20, QColor(5, 5, 5))
        qp.fillRect(50 + self.z5, 100, 50 + self.z5 + self.z6, 20, QColor(245, 250, 250))

    def update(self):
        try:
            self.tz1 = 10 * float(self.qDermis.text())
            self.tz2 = 10 * float(self.qFat.text())
            self.tz3 = 10 * float(self.qMuscle.text())
            self.tz4 = 10 * float(self.qDistance.text())
            self.tz5 = 10 * float(self.qLength.text())
            self.tz6 = 10 * float(self.qWidth.text())

            self.z1 = int(self.tz1)
            self.z2 = int(self.tz2)
            self.z3 = int(self.tz3)
            self.z4 = int(self.tz4)
            self.z5 = int(self.tz5)
            self.z6 = int(self.tz6)

            if any (z == None for z in [self.z1, self.z2, self.z3, self.z4, self.z5, self.z6]):
                QMessageBox.critical(self, 'Error', 'Please fill in all tissue parameters.')
                return

        except ValueError:
            QMessageBox.critical(self, 'Error', 'Invalid input. Please enter numeric values only.')
            return

        self.func = (self.drawTissue, {})
        self.modified = True
        self.repaint()

    """def drawTissue(self):
        try:
            if any(val == ' ' for val in
                   [self.z0, self.z1, self.z2, self.z3, self.z4, self.z5, self.z6, self.z7, self.z8, self.z9]):
                raise ValueError("Please fill in all tissue parameters.")
            if not (300 <= self.z0 <= 1000):
                raise ValueError("Wavelength must be between 300 and 1000 nm.")

            self.update()

        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))
    """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
