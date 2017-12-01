from PyQt5 import QtCore, QtGui, QtWidgets



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
        
