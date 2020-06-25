# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'test.ui'
# Created by: PyQt5 UI code generator 5.14.2
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

# Main Window UI design setting
# 전체적인 화면 구성 디자인
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(844, 487)
        self.count = 0
        self.duration_int = 5
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(40, 450, 111, 31))
        self.start.setObjectName("start")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 741, 111))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.aa = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.aa.setText("")
        self.aa.setPixmap(QtGui.QPixmap("img/aa.png"))
        self.aa.setAlignment(QtCore.Qt.AlignCenter)
        self.aa.setObjectName("aa")
        self.horizontalLayout.addWidget(self.aa)
        self.bb = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.bb.setText("")
        self.bb.setPixmap(QtGui.QPixmap("img/bb.png"))
        self.bb.setAlignment(QtCore.Qt.AlignCenter)
        self.bb.setObjectName("bb")
        self.horizontalLayout.addWidget(self.bb)
        self.cc = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.cc.setText("")
        self.cc.setPixmap(QtGui.QPixmap("img/cc.png"))
        self.cc.setAlignment(QtCore.Qt.AlignCenter)
        self.cc.setObjectName("cc")
        self.horizontalLayout.addWidget(self.cc)
        self.dd = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.dd.setText("")
        self.dd.setPixmap(QtGui.QPixmap("img/dd.png"))
        self.dd.setAlignment(QtCore.Qt.AlignCenter)
        self.dd.setObjectName("dd")
        self.horizontalLayout.addWidget(self.dd)
        self.screen = QtWidgets.QLabel(self.centralwidget)
        self.screen.setGeometry(QtCore.QRect(100, 130, 601, 311))
        self.screen.setText("")
        self.screen.setPixmap(QtGui.QPixmap("img/screen.png"))
        self.screen.setAlignment(QtCore.Qt.AlignCenter)
        self.screen.setObjectName("screen")
        self.nextp = QtWidgets.QPushButton(self.centralwidget)
        self.nextp.setGeometry(QtCore.QRect(780, 450, 21, 31))
        self.nextp.setObjectName("nextp")
        self.timer = QtWidgets.QLabel(self.centralwidget)
        self.timer.setGeometry(QtCore.QRect(720, 130, 111, 31))
        self.timer.setStyleSheet("font: 16pt \"Arial\";")
        self.timer.setAlignment(QtCore.Qt.AlignCenter)
        self.timer.setObjectName("timer")
        self.icon = QtWidgets.QLabel(self.centralwidget)
        self.icon.setGeometry(QtCore.QRect(650, 330, 141, 131))
        self.icon.setText("")
        self.icon.setScaledContents(True)
        self.icon.setObjectName("icon")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 440, 841, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.click = QtWidgets.QPushButton(self.centralwidget)
        self.click.setGeometry(QtCore.QRect(742, 330, 51, 28))
        self.click.hide()
        self.click.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.click.setObjectName("click")
        self.line.raise_()
        self.start.raise_()
        self.horizontalLayoutWidget.raise_()
        self.screen.raise_()
        self.nextp.raise_()
        self.timer.raise_()
        self.icon.raise_()
        self.click.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # when each button clicked - events
        self.start.clicked.connect(self.show_timer)
        self.nextp.clicked.connect(self.nextpage)
        self.click.clicked.connect(self.show_result)

    # change the UI - 화면 전환
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start.setText(_translate("MainWindow", "Start Statistics"))
        self.nextp.setText(_translate("MainWindow", ">"))
        self.timer.setText(_translate("MainWindow", ""))
        self.click.setText(_translate("MainWindow", "Click"))
    # flow 연결되도록 function
    def nextpage(self):
        self.count += 1
        print(self.count)
        if self.count == 1:
            self.screen.setPixmap(QtGui.QPixmap("img/sc2.png"))
        elif self.count == 2:
            app = QtCore.QCoreApplication([])
            #start_timer(timer_func, 10)
            self.show_icon()
        elif self.count ==3:
            self.screen.setPixmap(QtGui.QPixmap("img/screen.png"))

    #set the timer
    def show_timer(self):
        msg = QMessageBox()
        msg.setWindowTitle("Set the Timer")
        msg.setText("Timer 01 : 00")

        # when OK btn clicked - timer start
        x = msg.exec_()
        print("closed")

    #show a statistics result
    def show_result(self):
        self.icon.hide()
        self.click.hide()

        msg = QMessageBox()
        msg.setWindowTitle("Quiz Results")
        msg.setIconPixmap(QtGui.QPixmap("img/result.png"))

        x = msg.exec_()
        self.nextpage()
    # show icon - Start the statistics
    def show_icon(self):
        self.icon.setPixmap(QtGui.QPixmap("img/mini.png"))
        self.click.show()

#start the timer
def start_timer(slot, countt=0, interval=1000):
    counter = 10
    def handler():
        nonlocal counter
        counter -= 1
        slot(counter)
        if counter == countt:
            timer.stop()
            timer.deleteLater()

    timer = QtCore.QTimer()
    timer.timeout.connect(handler)
    timer.start(interval)
# time remaining display
def timer_func(countt):
    print('Timer:', countt)
    Ui_MainWindow.timer.setText('T:', countt)
    if countt == 0:
        QtCore.QCoreApplication.quit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())