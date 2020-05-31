import cv2
import threading
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon

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


def sound_alarm(path):
	# play an alarm sound
	playsound.playsound(path)

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-r", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-a", "--alarm", type=str, default="",
	help="path alarm .WAV file")
ap.add_argument("-w", "--webcam", type=int, default=0,
	help="index of webcam on system")
args = vars(ap.parse_args())

#eye detection

running = False
def run():
    EYE_AR_THRESH = 0.19
    EYE_AR_CONSEC_FRAMES = 60

    COUNTER = 0
    ALARM_ON = False

    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    time.sleep(2.0)
    i = 0
    j = 0
    c = 0
    
    global running
    cap = cv2.VideoCapture('hapum.mov')
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    label.resize(width, height)

    cap2 = cv2.VideoCapture('nnn.mov')
    cap3 = cv2.VideoCapture('nabc.mov')
    cap4 = cv2.VideoCapture('fff.mov')

    # 친구 얼굴 1
    pixmap5 = QtGui.QPixmap('aaa.png')
    label3.setPixmap(pixmap5)
    label3.show()

    pixmap3 = QtGui.QPixmap('aaa.png')
    label4.setPixmap(pixmap3)
    label4.show()

    pixmap4 = QtGui.QPixmap('aaa.png')
    label5.setPixmap(pixmap4)
    label5.show()

    #learning objective 칸
    pixmap2 = QtGui.QPixmap('ll.png')
    label2.setPixmap(pixmap2)
    label2.show()

    C = 0
    while running:
        # if(cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT)):
        #     capture.open("detection.mov")
        ret4, img4 = cap4.read() 
        ret3, img3 = cap3.read() 
        ret2, img2 = cap2.read()
        ret, img = cap.read()
        img = imutils.resize(img, width=700)
        img2 = imutils.resize(img2, width = 200)
        img3 = imutils.resize(img3, width=200)
        img4 = imutils.resize(img4, width=200)
        h,w,c = img.shape

        if ret:
            # cv2.putText(img, "CHEER UP!", (300, 150), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (250,250,250), 2)
	        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h,w,c = img.shape

            # detect faces in the grayscale frame, 얼굴 인식하는 거. 
            rects = detector(img, 0)

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

def onExit():
    print("exit")
    stop()

app = QtWidgets.QApplication([])
win = QtWidgets.QWidget()

vbox = QtWidgets.QVBoxLayout()
horizontal_layout1 = QtWidgets.QHBoxLayout()
horizontal_layout2 = QtWidgets.QHBoxLayout()
vertical_layout = QtWidgets.QVBoxLayout()

label = QtWidgets.QLabel()
label2 = QtWidgets.QLabel()
label2.resize(100, 300)

label3 = QtWidgets.QLabel()
label4 = QtWidgets.QLabel()
label5 = QtWidgets.QLabel()
label6 = QtWidgets.QLabel()

btn_start = QtWidgets.QPushButton("Camera On")
btn_stop = QtWidgets.QPushButton("Camera Off")

horizontal_layout1.addWidget(label3)
horizontal_layout1.addWidget(label4)
horizontal_layout1.addWidget(label5)
# horizontal_layout1.addWidget(label6)

horizontal_layout2.addWidget(label)
horizontal_layout2.addWidget(label2)

vertical_layout.addLayout(horizontal_layout1)
vertical_layout.addLayout(horizontal_layout2)
vertical_layout.addWidget(btn_start)
vertical_layout.addWidget(btn_stop)

win.setWindowTitle('New Zoom')
# win.setLayout(vbox)
# win.resize(1000, 800)
win.setLayout(vertical_layout)
win.show()

btn_start.clicked.connect(start)
btn_stop.clicked.connect(stop)
app.aboutToQuit.connect(onExit)

sys.exit(app.exec_())