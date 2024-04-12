from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
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

        self.initUI()
    def initUI(self):
        self.titleLb = QtWidgets.QLabel('Monte-Carlo modeling of optical sensors for postoperative free flap monitoring', self)
        self.titleLb.setFont(self.titleFont)
        self.titleLb.setStyleSheet('color: palevioletred;')
        self.titleLb.setGeometry(200, 0, 2000, 80)

        self.lb1 = QtWidgets.QLabel('1. Choose wavelength from 300 to 1000 [nm]:', self)
        self.lb1.setFont(self.regularFont)
        self.lb1.setGeometry(60, 90, 500, 40)

        self.q1 = QtWidgets.QLineEdit(self)
        self.q1.setFont(self.lineFont)
        self.q1.setMaxLength(4)
        self.q1.setTextMargins(60, 2, 60, 2)
        self.q1.setFrame(True)
        self.q1.setGeometry(60, 130, 180, 30)

        self.lb2 = QtWidgets.QLabel('2. Choose tissue parameters:', self)
        self.lb2.setFont(self.regularFont)
        self.lb2.setGeometry(60, 180, 500, 40)

        self.lbDermis = QtWidgets.QLabel('• Dermis [1-5 mm]', self)
        self.lbDermis.setFont(self.smallFont)
        self.lbDermis.setGeometry(60, 220, 200, 30)

        self.qDermis = QtWidgets.QLineEdit(self)
        self.qDermis.setFont(self.lineFont)
        self.qDermis.setMaxLength(2)
        self.qDermis.setTextMargins(35, 2, 35, 2)
        self.qDermis.setFrame(True)
        self.qDermis.setGeometry(60, 250, 100, 30)

        self.lbFat = QtWidgets.QLabel('• Fat [1-15 mm]', self)
        self.lbFat.setFont(self.smallFont)
        self.lbFat.setGeometry(280, 220, 200, 30)

        self.qFat = QtWidgets.QLineEdit(self)
        self.qFat.setFont(self.lineFont)
        self.qFat.setMaxLength(2)
        self.qFat.setTextMargins(35, 2, 35, 2)
        self.qFat.setFrame(True)
        self.qFat.setGeometry(280, 250, 100, 30)

        self.lbMuscle = QtWidgets.QLabel('• Muscle [1-20 mm]', self)
        self.lbMuscle.setFont(self.smallFont)
        self.lbMuscle.setGeometry(500, 220, 200, 30)

        self.qMuscle = QtWidgets.QLineEdit(self)
        self.qMuscle.setFont(self.lineFont)
        self.qMuscle.setMaxLength(2)
        self.qMuscle.setTextMargins(35, 2, 35, 2)
        self.qMuscle.setFrame(True)
        self.qMuscle.setGeometry(500, 250, 100, 30)

        self.lbDistance = QtWidgets.QLabel('• Distance [1-10 mm]', self)
        self.lbDistance.setFont(self.smallFont)
        self.lbDistance.setGeometry(60, 300, 200, 30)

        self.qDistance = QtWidgets.QLineEdit(self)
        self.qDistance.setFont(self.lineFont)
        self.qDistance.setMaxLength(2)
        self.qDistance.setTextMargins(35, 2, 35, 2)
        self.qDistance.setFrame(True)
        self.qDistance.setGeometry(60, 330, 100, 30)

        self.lbLength = QtWidgets.QLabel('• Length [1-10 mm]', self)
        self.lbLength.setFont(self.smallFont)
        self.lbLength.setGeometry(280, 300, 200, 30)

        self.qLength = QtWidgets.QLineEdit(self)
        self.qLength.setFont(self.lineFont)
        self.qLength.setMaxLength(2)
        self.qLength.setTextMargins(35, 2, 35, 2)
        self.qLength.setFrame(True)
        self.qLength.setGeometry(280, 330, 100, 30)

        self.lbWidth = QtWidgets.QLabel('• Width [1-10 mm]', self)
        self.lbWidth.setFont(self.smallFont)
        self.lbWidth.setGeometry(500, 300, 200, 30)

        self.qWidth = QtWidgets.QLineEdit(self)
        self.qWidth.setFont(self.lineFont)
        self.qWidth.setMaxLength(2)
        self.qWidth.setTextMargins(35, 2, 35, 2)
        self.qWidth.setFrame(True)
        self.qWidth.setGeometry(500, 330, 100, 30)

        self.lb3 = QtWidgets.QLabel('3. Tissue representation:', self)
        self.lb3.setFont(self.regularFont)
        self.lb3.setGeometry(60, 380, 500, 40)

        self.lb4 = QtWidgets.QLabel('4. Choose simulation parameters:', self)
        self.lb4.setFont(self.regularFont)
        self.lb4.setGeometry(60, 850, 500, 40)

        self.lbPhotons = QtWidgets.QLabel('• Number of photons:', self)
        self.lbPhotons.setFont(self.smallFont)
        self.lbPhotons.setGeometry(60, 890, 400, 30)

        self.qPhotons = QtWidgets.QLineEdit(self)
        self.qPhotons.setFont(self.lineFont)
        self.qPhotons.setMaxLength(2)
        self.qPhotons.setTextMargins(35, 2, 35, 2)
        self.qPhotons.setFrame(True)
        self.qPhotons.setGeometry(60, 920, 100, 30)

        self.lbAnizo = QtWidgets.QLabel('• Anisotropy [-0.9 - 0.9]:', self)
        self.lbAnizo.setFont(self.smallFont)
        self.lbAnizo.setGeometry(300, 890, 400, 30)

        self.qAnizo = QtWidgets.QLineEdit(self)
        self.qAnizo.setFont(self.lineFont)
        self.qAnizo.setMaxLength(2)
        self.qAnizo.setTextMargins(35, 2, 35, 2)
        self.qAnizo.setFrame(True)
        self.qAnizo.setGeometry(300, 920, 100, 30)

        self.lbIndex = QtWidgets.QLabel('• Index of refraction medium [1.1 - 20]:', self)
        self.lbIndex.setFont(self.smallFont)
        self.lbIndex.setGeometry(540, 890, 400, 30)

        self.qIndex = QtWidgets.QLineEdit(self)
        self.qIndex.setFont(self.lineFont)
        self.qIndex.setMaxLength(2)
        self.qIndex.setTextMargins(35, 2, 35, 2)
        self.qIndex.setFrame(True)
        self.qIndex.setGeometry(540, 920, 100, 30)

        self.btnDraw = QtWidgets.QPushButton('Draw tissue representation', self)
        self.btnDraw.setStyleSheet('background-color: pink; color: black;')
        self.btnDraw.setFont(self.smallFont)
        self.btnDraw.setGeometry(1000, 150, 360, 50)
        self.btnDraw.clicked.connect(self.drawTissue)

        self.btnSave = QtWidgets.QPushButton('Save the data to the file', self)
        self.btnSave.setStyleSheet('background-color: pink; color: black;')
        self.btnSave.setFont(self.smallFont)
        self.btnSave.setGeometry(1000, 230, 360, 50)

        self.btnFile = QtWidgets.QPushButton('Choose the file', self)
        self.btnFile.setStyleSheet('background-color: pink; color: black;')
        self.btnFile.setFont(self.smallFont)
        self.btnFile.setGeometry(1490, 150, 360, 50)

        self.btnSim = QtWidgets.QPushButton('Start simulation', self)
        self.btnSim.setStyleSheet('background-color: pink; color: black;')
        self.btnSim.setFont(self.smallFont)
        self.btnSim.setGeometry(1490, 230, 360, 50)

        self.z0 = 0
        self.z1 = 0
        self.z2 = 0
        self.z3 = 0
        self.z4 = 0
        self.z5 = 0
        self.z6 = 0
        self.z7 = 0
        self.z8 = 0
        self.z9 = 0

    def paintEvent(self, e):
        self.tissueCanva = QPainter(self)
        self.tissueCanva.setBrush(QColor('white'))
        self.tissueCanva.drawRect(60, 430, 600, 400)

        self.resultCanva = QPainter(self)
        self.resultCanva.setBrush(QColor('white'))
        self.resultCanva.drawRect(1000, 310, 850, 600)

        """ if self.z1 is not None and self.z2 is not None and self.z3 is not None and self.z5 is not None and self.z7 is not None:
            self.tissueCanva.fillRect(25, 25, 325, 25 + 5 * self.z1, QColor(247, 231, 210))
            self.tissueCanva.fillRect(25, 25 + 5 * self.z1, 325, 25 + 5 * (self.z1 + self.z2), QColor(242, 224, 145))
            self.tissueCanva.fillRect(25, 25 + 5 * (self.z1 + self.z2), 325, 25 + 5 * (self.z1 + self.z2 + self.z3), QColor(237, 202, 223))
            self.tissueCanva.fillRect(50, 25, 45, 20, QColor(5, 5, 5))
            self.tissueCanva.fillRect(50 + 22.5 * self.z5, 25, 50 + 22.5 * self.z5 + self.z6, 20, QColor(245, 250, 250))
        """
    def drawTissue(self):
        try:
            if any(z == ' ' for z in
                   [self.z0, self.z1, self.z2, self.z3, self.z4, self.z5, self.z6, self.z7, self.z8, self.z9]):
                raise ValueError("Please fill in all tissue parameters.")
            if not (300 <= self.z0 <= 1000):
                raise ValueError("Wavelength must be between 300 and 1000 nm.")
            else:
                self.z0 = int(self.q1.text())
                self.z1 = int(self.qDermis.text())
                self.z2 = int(self.qFat.text())
                self.z3 = int(self.qMuscle.text())
                self.z4 = int(self.qDistance.text())
                self.z5 = int(self.qLength.text())
                self.z6 = int(self.qWidth.text())
                self.z7 = int(self.qPhotons.text())
                self.z8 = int(self.qAnizo.text())
                self.z9 = int(self.qIndex.text())

        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
