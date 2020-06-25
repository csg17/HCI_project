import cv2
import threading
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import (QApplication,QLabel, QDialog, QWidget, QGroupBox, QRadioButton, QCheckBox, QPushButton, QMenu, QGridLayout, QVBoxLayout, QHBoxLayout)

from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread

from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import datetime
import math
import playsound
import argparse
import imutils
import time
import dlib
import csv
import numpy as np

def CreateCheckBox(self):
        self.groupbox = QGroupBox("How much are you understanding? :-)")
        self.groupbox.setFont(QtGui.QFont("Times", 17))
        vboxLayout = QVBoxLayout()

        self.check1 = QCheckBox("Good")
        self.check1.setIcon(QtGui.QIcon("smile.png"))
        self.check1.setIconSize(QtCore.QSize(40, 40))
        self.check1.setFont(QtGui.QFont("Times", 15))
        vboxLayout.addWidget(self.check1)

        self.check2 = QCheckBox("So..so..")
        self.check2.setIcon(QtGui.QIcon("soso.png"))
        self.check2.setIconSize(QtCore.QSize(40, 40))
        self.check2.setFont(QtGui.QFont("Times", 15))
        vboxLayout.addWidget(self.check2)

        self.check3 = QCheckBox("Not well..")
        self.check3.setIcon(QtGui.QIcon("notwell.png"))
        self.check3.setIconSize(QtCore.QSize(40, 40))
        self.check3.setFont(QtGui.QFont("Times", 15))
        vboxLayout.addWidget(self.check3)

        self.groupbox.setLayout(vboxLayout)

running = False

def run():

    time.sleep(2.0)
    i = 0
    j = 0
    c = 0
    
    # btn_ll.clicked.connect(change1)
    # btn_tl.clicked.connect(change2)

    global running
    cap = cv2.VideoCapture('hapum.mov')
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    label.resize(width, height)

    # 친구 얼굴 1
    pixmap5 = QtGui.QPixmap('2.png')
    label3.setPixmap(pixmap5)
    label3.show()
    
    # 친구 얼굴 2
    pixmap3 = QtGui.QPixmap('2.png')
    label4.setPixmap(pixmap3)
    label4.show()
    
    # 친구 얼굴 3
    pixmap4 = QtGui.QPixmap('3.png')
    label5.setPixmap(pixmap4)
    label5.show()
    
    # 친구 얼굴 4
    pixmap6 = QtGui.QPixmap('4.png')
    label6.setPixmap(pixmap6)
    label6.show()

    #learning objective 칸
    pixmap2 = QtGui.QPixmap('ll1.png')
    label2.setPixmap(pixmap2)
    label2.show()

    C = 0
    while running:
        ret, img = cap.read()
        img = imutils.resize(img, width = 800)

        if ret:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h,w,c = img.shape

            # cv2를 Pixmap으로.
            qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            label.setPixmap(pixmap)
        else:
            QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
            print("cannot read frame.")
            break

    cap.release()
    print("Thread end.")

def stop():
    global running
    running = False
    print("stoped..")

def start():
    global running
    running = True
    th = threading.Thread(target=run)
    th.start()
    print("started..")

def change1():
    pix = QtGui.QPixmap('ll.png')
    label2.setPixmap(pix)
    label2.show()

def change2():
    pix = QtGui.QPixmap('ll2.png')
    label2.setPixmap(pix)
    label2.show()
    print("hi")

def onExit():
    print("exit")
    stop()

app = QtWidgets.QApplication([])
win = QtWidgets.QWidget()
CreateCheckBox(win)
 
vbox = QtWidgets.QVBoxLayout()
horizontal_layout1 = QtWidgets.QHBoxLayout()
horizontal_layout2 = QtWidgets.QHBoxLayout()
horizontal_layout3 = QtWidgets.QHBoxLayout()
vertical_layout = QtWidgets.QVBoxLayout()
vertical_layout2 = QtWidgets.QVBoxLayout()

# label은 '학생 얼굴 화면'
label = QtWidgets.QLabel()

# label2는 오른쪽에 띄울 화면
label2 = QtWidgets.QLabel()
label2.resize(100, 300)

# label3~6은 zoom 친구들 화면
label3 = QtWidgets.QLabel()
label4 = QtWidgets.QLabel()
label5 = QtWidgets.QLabel()
label6 = QtWidgets.QLabel()

btn_start = QtWidgets.QPushButton("Camera On")
btn_stop = QtWidgets.QPushButton("Camera Off")
btn_ll = QtWidgets.QPushButton("Learning Obj")
btn_tl = QtWidgets.QPushButton("Time Line")

horizontal_layout1.addWidget(label3)
horizontal_layout1.addWidget(label4)
horizontal_layout1.addWidget(label5)
horizontal_layout1.addWidget(label6)

vertical_layout2.addWidget(label2)
vertical_layout2.addWidget(win.groupbox)

horizontal_layout2.addWidget(label)
horizontal_layout2.addLayout(vertical_layout2)

vertical_layout.addLayout(horizontal_layout1)
vertical_layout.addLayout(horizontal_layout2)
vertical_layout.addWidget(btn_start)
vertical_layout.addWidget(btn_stop)

win.setWindowTitle('New Zoom')
win.setLayout(vertical_layout)

win.show()

btn_start.clicked.connect(start)
print("hi")
btn_stop.clicked.connect(stop)
btn_ll.clicked.connect(change2)

app.aboutToQuit.connect(onExit)

sys.exit(app.exec_())
