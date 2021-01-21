from PyQt5 import QtCore, QtGui, QtWidgets
from login import Ui_Login_Form

class Ui_MainWindow(object):
    def login_form(self):
        self.LoginWindow = QtWidgets.QMainWindow()
        self.ui = Ui_Login_Form()
        self.ui.setupUi(self.LoginWindow)
        self.LoginWindow.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)                                     #Size of the display window
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.welcome_label = QtWidgets.QLabel(self.centralwidget)           #Sets the label in the center of the screen
        self.welcome_label.setGeometry(QtCore.QRect(260, 150, 241, 71))     #Size of the label
        self.welcome_label.setObjectName("welcome_label")
        self.get_started_button = QtWidgets.QPushButton(self.centralwidget)     #Sets button on the center
        self.get_started_button.setGeometry(QtCore.QRect(320, 270, 111, 28))    #Size of the button
        self.get_started_button.setObjectName("get_started_button")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.get_started_button.clicked.connect(self.login_form)                #Button clicked go to function login_form
        self.get_started_button.clicked.connect(MainWindow.hide)                #Hide the current window
        #MainWindow.hide()
        #MainWindow.close()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "COVID-19 Project"))
        self.welcome_label.setText(_translate("MainWindow", "WELCOME TO THE COVID-19 PROJECT"))
        self.get_started_button.setText(_translate("MainWindow", "GET STARTED"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())