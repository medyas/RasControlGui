#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rasGUI.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import socketserver,subprocess
import RPi.GPIO as GPIO
from _thread import start_new_thread
from time import sleep
import signal, sys
import PyQt5

# variable init
a = 0
angle = 90
preAngle = 0
preSpeed = 0
speed = 0
strength = 0
add = ""
connected = ""
enabled = True

# orange GND
# purple 5V

# Servo config
serPin = 37
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(serPin, GPIO.OUT)# yellow 3
servopwm = GPIO.PWM(serPin, 50)
servopwm.start(7)

# DC motor config
fPin = 36
bPin = 38
ePin = 40
GPIO.setup(fPin,GPIO.OUT)# white 16 forwared
GPIO.setup(bPin,GPIO.OUT)# red 18 backward
GPIO.setup(ePin,GPIO.OUT)# black 22 enable

motorpwm = GPIO.PWM(ePin, 50)
motorpwm.start(0)


# Socket server class
class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        while True:
            global angle, strength ,speed, a, connected, appui, ui, enabled
            if(not enabled):
                # self.rfile is a file-like object created by the handler;
                # we can now use e.g. readline() instead of raw recv() calls
                self.data = self.request.recv(1024).strip()
                #self.rfile.readline().strip()
                if(a==0):
                    #print("{} wrote:".format(self.client_address[0]))
                    connected = "Connected ip: "+self.client_address[0]
                    appui.setCon(connected)
                    a+=1
                data = self.data.decode("utf-8").rstrip().strip("\n")
                if(data!= ""):
                    if(data == "disconnect"):
                        print("restarting")
                        a = 0
                        self.close()
                        sleep(1)
                        mainServer()
                    elif("gui" in data):
                        appui.hide()
                        ui.setGui()
                        enabled = True
                    else:    
                        temp = data.split(":")
                        angle = int(temp[0])
                        strength = int(temp[1])
                        speed = float(temp[2])
                        appui.update(speed, angle)
                        Servo()
                        Motor()
                                                                                      

            # Likewise, self.wfile is a file-like object used to write back
            # to the client
            #self.wfile.write(str(speed).encode("utf-8"))      





# *********************************************** #
class Ui_AppWindow(QtWidgets.QWidget):

    def __init__(self):
        super(Ui_AppWindow, self).__init__()
        self.setStyleSheet('background-color:#efefef; color:white;')
        global add, angle, speed, connected
        
        self.layout = QtWidgets.QVBoxLayout()
        
        self.label = QtWidgets.QLabel("\t\t"+add)
        self.label.setStyleSheet("color: #005C99;")
        self.layout.addWidget(self.label)
        
        self.label1 = QtWidgets.QLabel("\t\t"+connected)
        self.label1.setStyleSheet("color: #005C99;")
        self.layout.addWidget(self.label1)

        palette = QtGui.QPalette()
        palette.setColor(palette.WindowText, QtGui.QColor(85, 85, 255))
        palette.setColor(palette.Background, QtGui.QColor(0, 170, 255))
        palette.setColor(palette.Light, QtGui.QColor(0, 92, 153))
        palette.setColor(palette.Dark, QtGui.QColor(0, 92, 137))

        self.speed = QtWidgets.QLCDNumber(self)
        self.speed.setGeometry(QtCore.QRect(100, 100, 64, 23))
        self.speed.setObjectName("speed")
        self.speed.display(speed)
        self.speed.setPalette(palette)

        self.angle = QtWidgets.QLCDNumber(self)
        self.angle.setGeometry(QtCore.QRect(200, 100, 64, 23))
        self.angle.setObjectName("angle")
        self.angle.display(angle)
        self.angle.setPalette(palette)

        self.speed_lable = QtWidgets.QLabel("Speed")
        self.speed_lable.setGeometry(QtCore.QRect(100, 70, 47, 25))
        self.speed_lable.setObjectName("speed_lable")
        self.speed_lable.setStyleSheet('color:#00497a;')
        
        self.angle_lable = QtWidgets.QLabel("Angle")
        self.angle_lable.setGeometry(QtCore.QRect(200, 70, 47, 25))
        self.angle_lable.setObjectName("angle_lable")
        self.angle_lable.setStyleSheet('color:#00497a;')

        self.hbl = QtWidgets.QHBoxLayout()
        self.hbl.addWidget(self.speed_lable)
        self.hbl.addWidget(self.angle_lable)
        self.layout.addLayout(self.hbl)
        
        self.hb = QtWidgets.QHBoxLayout()
        self.hb.addWidget(self.speed)
        self.hb.addWidget(self.angle)
        self.layout.addLayout(self.hb)
        
        self.setWindowTitle("RasControl GUI: Android Control")
        self.setLayout(self.layout)
        self.setGeometry(100, 100, 400, 200)

        a = self.angle
        s = self.speed

    def update(self, speed, angle):
        self.angle.display(angle)
        self.speed.display(speed)

    def setIp(self, add):
        self.label.setText(add)

    def setCon(self, c):
        self.label1.setText(c)
        
# *********************************************** #    
class Ui_ButtonHelpWindow(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_ButtonHelpWindow, self).__init__()
        self.setStyleSheet('background-color:#005C99; color:white;')
        self.vb = QtWidgets.QVBoxLayout()
        self.vb.addWidget(QtWidgets.QLabel('Button Control Help:'))
        self.vb.addWidget(QtWidgets.QLabel('This tab allows you to control the Raspberry with button.'))
        self.vb.addWidget(QtWidgets.QLabel('If you click one of the buttons: '))
        self.vb.addWidget(QtWidgets.QLabel('The forward and backward buttons will add or decrease a 20% to the current speed.'))
        self.vb.addWidget(QtWidgets.QLabel('The left and right buttons will add or decrease 10° angles.'))
        self.vb.addWidget(QtWidgets.QLabel('The stop button will set the speed to 0% and the angle to 90°.'))
        self.setLayout(self.vb)
        self.setWindowTitle("RasControl GUI: Button Control Help")
        self.setGeometry(100, 100, 400, 250)

class Ui_SliderHelpWindow(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_SliderHelpWindow, self).__init__()
        self.setStyleSheet('background-color:#005C99; color:white;')
        self.vb = QtWidgets.QVBoxLayout()
        self.vb.addWidget(QtWidgets.QLabel('Slider Control Help:'))
        self.vb.addWidget(QtWidgets.QLabel('This tab allows you to control the Raspberry with sliders.'))
        self.vb.addWidget(QtWidgets.QLabel('You can click or move each slider and based on that, The angle and speed will be set.'))
        self.vb.addWidget(QtWidgets.QLabel('If you click on the speed slider, based on the direction of the click the speed '))
        self.vb.addWidget(QtWidgets.QLabel("will be increased or decreased by 20%."))
        self.vb.addWidget(QtWidgets.QLabel("If you click on the angle slider, based on the direction of the click the angle "))
        self.vb.addWidget(QtWidgets.QLabel("will be increased or decreased by 10°."))
        self.vb.addWidget(QtWidgets.QLabel('The stop button will set the speed to 0% and the angle to 90°.'))
        self.setLayout(self.vb)
        self.setWindowTitle("RasControl GUI: Slider Control Help")
        self.setGeometry(100, 100, 400, 250)

# *********************************************** #
class Ui_AboutWindow(QtWidgets.QWidget):

    def __init__(self):
        super(Ui_AboutWindow, self).__init__()
        self.setStyleSheet('background-color:#003d66; color:white;')
        self.layout = QtWidgets.QVBoxLayout()
        
        pic = QtWidgets.QLabel(self)
        pic.setPixmap(QtGui.QPixmap("raspberry-pi-logo.png").scaled(128,160))
        
        self.layout.addWidget(QtWidgets.QLabel("About:"))
        self.layout.addWidget(QtWidgets.QLabel("This app is created as part of the RasControl Project,"))
        self.layout.addWidget(QtWidgets.QLabel("It allows you to control a DC motor and a servo motor that"))
        self.layout.addWidget(QtWidgets.QLabel("are connected to the raspberry pi."))
        self.layout.addWidget(QtWidgets.QLabel("\t\tCreated by ©Medyas"))


        iset = QtWidgets.QLabel(self)
        iset.setPixmap(QtGui.QPixmap("isetr.png").scaled(400,90)) 
        self.layout.addWidget(iset)

        
        
        self.hb = QtWidgets.QHBoxLayout()
        
        self.hb.addWidget(pic)
        self.hb.addLayout(self.layout)

        
        
        self.setWindowTitle("RasControl GUI: About")
        self.setLayout(self.hb)
        self.setGeometry(100, 100, 400, 200)

# ------------------------------------------------------------------ #
# main windows setup
class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("RasControl GUI")
        MainWindow.resize(780, 460)
        self.main = MainWindow

        style = "background-color:#e6f5ff; color: #003d66; border-radius: 20px; font: bold;"
        style2 = "background-color:#003d66; color: #e6f5ff; border-radius: 20px; font: bold;"
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 780, 460))
        self.tabWidget.setObjectName("tabWidget")
        
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")

        palette = QtGui.QPalette()
        palette.setColor(palette.WindowText, QtGui.QColor(85, 85, 255))
        palette.setColor(palette.Background, QtGui.QColor(0, 170, 255))
        palette.setColor(palette.Light, QtGui.QColor(153, 214, 255))
        palette.setColor(palette.Dark, QtGui.QColor(0, 92, 153))
        
        self.speed_slider = QtWidgets.QSlider(self.tab_1)
        self.speed_slider.setGeometry(QtCore.QRect(50, 20, 51, 300))
        self.speed_slider.setMinimum(-100)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setSingleStep(20)
        self.speed_slider.setPageStep(20)
        self.speed_slider.setProperty("value", 0)
        self.speed_slider.setOrientation(QtCore.Qt.Vertical)
        self.speed_slider.setObjectName("speed_slider")
        self.speed_slider.valueChanged.connect(self.getSpeed)
        
        self.speed = QtWidgets.QLCDNumber(self.tab_1)
        self.speed.setGeometry(QtCore.QRect(120, 160, 64, 23))
        self.speed.setObjectName("speed")
        self.speed.setPalette(palette)

        self.speed_lable = QtWidgets.QLabel(self.tab_1)
        self.speed_lable.setGeometry(QtCore.QRect(130, 130, 47, 25))
        self.speed_lable.setObjectName("speed_lable")
        self.speed_lable.setStyleSheet('color:#00497a;')
        
        self.angle_slider = QtWidgets.QSlider(self.tab_1)
        self.angle_slider.setGeometry(QtCore.QRect(230, 290, 350, 51))
        self.angle_slider.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.angle_slider.setMinimum(0)
        self.angle_slider.setMaximum(180)
        self.angle_slider.setSingleStep(10)
        self.angle_slider.setPageStep(10)
        self.angle_slider.setProperty("value", 90)
        self.angle_slider.setSliderPosition(90)
        self.angle_slider.setOrientation(QtCore.Qt.Horizontal)
        self.angle_slider.setObjectName("angle_slider")
        self.angle_slider.valueChanged.connect(self.getAngle)

        self.angle = QtWidgets.QLCDNumber(self.tab_1)
        self.angle.setGeometry(QtCore.QRect(370, 250, 64, 23))
        self.angle.setObjectName("angle")
        self.angle.display(90)
        self.angle.setPalette(palette)

        self.angle_lable = QtWidgets.QLabel(self.tab_1)
        self.angle_lable.setGeometry(QtCore.QRect(380, 220, 47, 25))
        self.angle_lable.setObjectName("angle_lable")
        self.angle_lable.setStyleSheet('color:#00497a;')

        self.sStop = QtWidgets.QPushButton(self.tab_1)
        self.sStop.setGeometry(QtCore.QRect(360, 120, 91, 41))
        self.sStop.setObjectName("stop")
        self.sStop.setStyleSheet(style)
        self.sStop.clicked.connect(self.setSStop)

        self.squit = QtWidgets.QPushButton(self.tab_1)
        self.squit.setGeometry(QtCore.QRect(670, 340, 91, 41))
        self.squit.setObjectName("quit")
        self.squit.setStyleSheet(style2)
        self.squit.clicked.connect(self.windowQuit)
        
        self.toolButton_2 = QtWidgets.QToolButton(self.tab_1)
        self.toolButton_2.setGeometry(QtCore.QRect(750, 0, 25, 19))
        self.toolButton_2.setObjectName("toolButton_2")
        self.sliderhelpWindow = Ui_SliderHelpWindow()

        self.saction1 = QtWidgets.QAction(QtGui.QIcon("help.png"), u"Help")
        self.saction2 = QtWidgets.QAction(QtGui.QIcon("about.png"), u"About")

        self.popupMenu = QtWidgets.QMenu()
        self.popupMenu.addAction(self.saction1)
        self.popupMenu.addAction(self.saction2)

        self.saction1.triggered.connect(self.sliderHelp)
        self.saction2.triggered.connect(self.about)

        self.toolButton_2.setMenu( self.popupMenu )
        self.toolButton_2.setDefaultAction( self.saction1 )
        self.toolButton_2.setPopupMode( QtWidgets.QToolButton.InstantPopup )
        
        self.tabWidget.addTab(self.tab_1, "")
        
        # ************************ #
        
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        
        self.forward = QtWidgets.QPushButton(self.tab_2)
        self.forward.setGeometry(QtCore.QRect(330, 130, 91, 41))
        self.forward.setObjectName("forward")
        self.forward.setStyleSheet(style)
        self.forward.clicked.connect(self.setForward)
        
        self.backward = QtWidgets.QPushButton(self.tab_2)
        self.backward.setGeometry(QtCore.QRect(330, 290, 91, 41))
        self.backward.setObjectName("backward")
        self.backward.setStyleSheet(style)
        self.backward.clicked.connect(self.setBackward)
        
        self.left = QtWidgets.QPushButton(self.tab_2)
        self.left.setGeometry(QtCore.QRect(200, 210, 91, 41))
        self.left.setObjectName("left")
        self.left.setStyleSheet(style)
        self.left.clicked.connect(self.setLeft)
        
        self.right = QtWidgets.QPushButton(self.tab_2)
        self.right.setGeometry(QtCore.QRect(470, 210, 91, 41))
        self.right.setObjectName("right")
        self.right.setStyleSheet(style)
        self.right.clicked.connect(self.setRight)
        
        self.bStop = QtWidgets.QPushButton(self.tab_2)
        self.bStop.setGeometry(QtCore.QRect(330, 210, 91, 41))
        self.bStop.setObjectName("stop")
        self.bStop.setStyleSheet(style)
        self.bStop.clicked.connect(self.setBStop)

        self.bquit = QtWidgets.QPushButton(self.tab_2)
        self.bquit.setGeometry(QtCore.QRect(670, 340, 91, 41))
        self.bquit.setObjectName("quit")
        self.bquit.setStyleSheet(style2)
        self.bquit.clicked.connect(self.windowQuit)
        
        self.toolButton = QtWidgets.QToolButton(self.tab_2)
        self.toolButton.setGeometry(QtCore.QRect(750, 0, 25, 19))
        self.toolButton.setObjectName("toolButton")

        self.baction1 = QtWidgets.QAction(QtGui.QIcon("help.png"), u"Help")
        self.baction2 = QtWidgets.QAction(QtGui.QIcon("about.png"), u"About")

        self.popupMenu = QtWidgets.QMenu()
        self.popupMenu.addAction(self.baction1)
        self.popupMenu.addAction(self.baction2)

        self.baction1.triggered.connect(self.buttonHelp)
        self.baction2.triggered.connect(self.about)

        self.toolButton.setMenu( self.popupMenu )
        self.toolButton.setDefaultAction( self.baction1 )
        self.toolButton.setPopupMode( QtWidgets.QToolButton.InstantPopup )

        self.buttonhelpWindow = Ui_ButtonHelpWindow()
        
        self.speed_2 = QtWidgets.QLCDNumber(self.tab_2)
        self.speed_2.setGeometry(QtCore.QRect(260, 50, 64, 23))
        self.speed_2.setObjectName("speed_2")
        self.speed_2.setPalette(palette)
        
        self.angle_2 = QtWidgets.QLCDNumber(self.tab_2)
        self.angle_2.setGeometry(QtCore.QRect(430, 50, 64, 23))
        self.angle_2.setObjectName("angle_2")
        self.angle_2.setPalette(palette)
        
        self.speed_lable_2 = QtWidgets.QLabel(self.tab_2)
        self.speed_lable_2.setGeometry(QtCore.QRect(270, 20, 47, 25))
        self.speed_lable_2.setObjectName("speed_lable_2")
        self.speed_lable_2.setStyleSheet('color:#00497a;')
        
        self.angle_lable_2 = QtWidgets.QLabel(self.tab_2)
        self.angle_lable_2.setGeometry(QtCore.QRect(442, 20, 47, 25))
        self.angle_lable_2.setObjectName("angle_lable_2")
        self.angle_lable_2.setStyleSheet('color:#00497a;')
        
        self.tabWidget.addTab(self.tab_2, "")

        # ************************ #
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 809, 21))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuSwitch = QtWidgets.QMenu(self.menubar)
        self.menuSwitch.setObjectName("menuSwitch")
        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.actionAbout = QtWidgets.QAction(QtGui.QIcon("about.png"), u'About')
        self.actionAbout.setObjectName("actionAbout")

        self.actionSwitchapp = QtWidgets.QAction(QtGui.QIcon("android3.png"), u'Switch to App')
        self.actionSwitchapp.setObjectName("actionSwitchapp")

        self.actionSwitchgui = QtWidgets.QAction(QtGui.QIcon("raspberry-pi-logo.png"), u'Switch to GUI')
        self.actionSwitchgui.setObjectName("actionSwitchgui")
        
        self.aboutui = Ui_AboutWindow()

        self.actionwindowf = QtWidgets.QAction(QtGui.QIcon("full.png"), u'Switch to FullScreen')
        self.actionwindowf.setObjectName("actionShowFull")
        self.actionwindown = QtWidgets.QAction(QtGui.QIcon("normal.png"), u'Switch to Normal')
        self.actionwindown.setObjectName("actionShowNormal")
        self.actionquit = QtWidgets.QAction(QtGui.QIcon("quit.png"), u'Quit')
        self.actionquit.setObjectName("actionquit")
        
        
        self.actionAbout.triggered.connect(self.about)
        self.actionSwitchapp.triggered.connect(self.app)
        self.actionSwitchgui.triggered.connect(self.gui)
        self.actionwindowf.triggered.connect(self.showf)
        self.actionwindown.triggered.connect(self.shown)
        self.actionquit.triggered.connect(self.windowQuit)
        
        self.menuAbout.addAction(self.actionwindowf)
        self.menuAbout.addSeparator()
        self.menubar.addAction(self.menuAbout.menuAction())
        
        self.menuAbout.addAction(self.actionwindown)
        self.menuAbout.addSeparator()
        self.menubar.addAction(self.menuAbout.menuAction())

        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addSeparator()
        self.menubar.addAction(self.menuAbout.menuAction())

        self.menuAbout.addAction(self.actionquit)
        self.menuAbout.addSeparator()
        self.menubar.addAction(self.menuAbout.menuAction())

        self.menuSwitch.addAction(self.actionSwitchapp)
        self.menuSwitch.addSeparator()
        self.menubar.addAction(self.menuSwitch.menuAction())

        self.menuSwitch.addAction(self.actionSwitchgui)
        self.menuSwitch.addSeparator()
        self.menubar.addAction(self.menuSwitch.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget.currentChanged.connect(self.changed)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RasControl GUI"))
        self.speed_lable.setText(_translate("MainWindow", "Speed"))
        self.angle_lable.setText(_translate("MainWindow", "Angle"))
        self.sStop.setText(_translate("MainWindow", "Stop"))
        self.bquit.setText(_translate("MainWindow", "Quit"))
        self.toolButton_2.setText(_translate("MainWindow", "..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Slider"))
        self.forward.setText(_translate("MainWindow", "Forward"))
        self.backward.setText(_translate("MainWindow", "Backward"))
        self.left.setText(_translate("MainWindow", "Left"))
        self.right.setText(_translate("MainWindow", "Right"))
        self.bStop.setText(_translate("MainWindow", "Stop"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.speed_lable_2.setText(_translate("MainWindow", "Speed"))
        self.angle_lable_2.setText(_translate("MainWindow", "Angle"))
        self.squit.setText(_translate("MainWindow", "Quit"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Button"))
        self.menuAbout.setTitle(_translate("MainWindow", "?"))
        self.menuSwitch.setTitle(_translate("MainWindow", "Switch"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionSwitchapp.setText(_translate("MainWindow", "Switch to app"))
        self.actionSwitchgui.setText(_translate("MainWindow", "Switch to GUI"))
        self.actionwindowf.setText(_translate("MainWindow", "Switch to FullScreen"))
        self.actionwindown.setText(_translate("MainWindow", "Switch to Normal"))
        self.actionquit.setText(_translate("MainWindow", "Quit"))

    def setGui(self):
        self.changed()
        self.tabWidget.setEnabled(True)

    def windowQuit(self):
        QtCore.QCoreApplication.instance().quit()

    def showf(self):
        self.main.showFullScreen()  

    def shown(self):
        self.main.showNormal()

    def about(self):
        self.aboutui.show()

    def app(self):
        self.changed()
        global enabled, appui, add
        appui.setIp("\t        Server: "+add)
        appui.show()
        self.tabWidget.setEnabled(False)
        enabled = False

    def gui(self):
        self.changed()
        global enabled, appui
        appui.hide()
        self.tabWidget.setEnabled(True)
        enabled = True
            

    def buttonHelp(self):
        self.buttonhelpWindow.show()

    def sliderHelp(self):
        self.sliderhelpWindow.show()

    def getSpeed(self):
        global speed
        speed = self.speed_slider.value()
        self.speed.display(speed)
        Motor()
    
    def getAngle(self):
        global angle
        angle = self.angle_slider.value()
        self.angle.display(angle)
        Servo()

    def setSStop(self):
        self.changed()

    def changed(self):
        global angle, speed
        angle = 90
        speed = 0
        self.speed.display(0)
        self.angle.display(90)
        self.speed_2.display(0)
        self.angle_2.display(90)
        self.speed_slider.setValue(0)
        self.angle_slider.setValue(90)
        Servo()
        Motor()

    def setBackward(self):
        global speed
        if speed>=-80:
            speed -= 20 
        self.speed_2.display(speed)
        Motor()

    def setForward(self):
        global speed
        if speed<=80:
            speed += 20 
        self.speed_2.display(speed)
        Motor()

    def setRight(self):
        global angle
        if angle>=10:
            angle -= 10
        self.angle_2.display(angle)
        Servo()

    def setLeft(self):
        global angle
        if angle<=170:
            angle += 10 
        self.angle_2.display(angle)
        Servo()

    def setBStop(self):
        self.changed()
        
# ********************************************* #

def mainServer():

    p = subprocess.Popen("ifconfig wlan0 | grep 'inet ' | cut -d' ' -f10", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    ip = p.stdout.readlines()[0].decode("utf-8").rstrip().strip("\n")
    port = 9999
    global add
    add = ip+":"+str(port)

    try:
        # Create the server, binding to localhost on port 9999
        server = socketserver.TCPServer((ip, port), MyTCPHandler)
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

        
    except(OSError):
        print("Something happend!")


# *********************************************** #  
# Servo motor control
def Servo():
    b = 0
    global preAngle, angle, strength, a
    if(not enabled):
        if(a!=0):
            if(angle==0 and b!=1 and strength==0):
                setCenter()
                b = 1
            elif(preAngle+3 >= angle and preAngle-3 <= angle):
                pass
            else:
                SetAngle(angle-180 if angle>=180 else angle)
                preAngle = angle
                b = 0
    else:
        SetAngle(angle)

# *********************************************** #
# set the servo to center (90degree)
def setCenter():
    GPIO.output(serPin, True)
    servopwm.ChangeDutyCycle(7)
    sleep(0.0001)
# *********************************************** #
# set the servo to angle
def SetAngle(angle):
    duty = angle / 18.0 + 2
    GPIO.output(serPin, True)
    servopwm.ChangeDutyCycle(duty)
    sleep(0.0001)

# *********************************************** #

# Motor control    
def Motor():
    global a, speed, preSpeed
    b = 0
    if(not enabled):
        if(a!=0):
            if(speed == 0 and b == 0):
                b = 1
                stop()
            elif(preSpeed+1 >= speed and preSpeed-1 <= speed):
                pass
            elif(speed != 0):
                preSpeed = speed
                b = 0
                forward(speed) if speed>0 else backward(speed)
    else:
        if(speed == 0):
            stop()
        else:
            forward(speed) if speed>0 else backward(speed)
                
                


# *********************************************** #
def stop():
    motorpwm.ChangeDutyCycle(0)
# *********************************************** #
def forward(speed):
    motorpwm.ChangeDutyCycle(speed) 
    GPIO.output(fPin,GPIO.HIGH)
    GPIO.output(bPin,GPIO.LOW)
    GPIO.output(ePin,GPIO.HIGH)
    sleep(0.0001)

# *********************************************** #
def backward(speed):
    motorpwm.ChangeDutyCycle(-speed) 
    GPIO.output(fPin,GPIO.LOW)
    GPIO.output(bPin,GPIO.HIGH)
    GPIO.output(ePin,GPIO.HIGH)
    sleep(0.0001)



# *********************************************** #

def main(f):
##    start_new_thread(Servo,())
##    start_new_thread(Motor,())
    
    start_new_thread(mainServer, ())

    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    global appui, ui
    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    appui = Ui_AppWindow()
    
    if(f == 1):
        MainWindow.showFullScreen()
    else:
        MainWindow.showNormal()
    sys.exit(app.exec_())

# ------------------------------------------------------------------ #

if __name__ == "__main__":

    main(1)
    
    

