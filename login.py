from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from AdminWindow import Ui_AdminWindow
from UserWindow import Ui_UserWindow

class Ui_Login_Form(object):

    def user_window(self):
        self.UserWindow = QtWidgets.QMainWindow()
        self.ui = Ui_UserWindow()
        self.ui.setupUi(self.UserWindow)
        self.UserWindow.show()

    def admin_window(self):
        self.AdminWindow = QtWidgets.QMainWindow()
        self.ui = Ui_AdminWindow()
        self.ui.setupUi(self.AdminWindow)
        self.AdminWindow.show()

    def messagebox(self,title,message):
        messa=QtWidgets.QMessageBox()
        messa.setWindowTitle(title)
        messa.setText(message)
        messa.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messa.exec_()

    def warningBox(self,title,message):   #working but terminating the project
        messa=QtWidgets.QMessageBox()
        messa.setWindowTitle(title)
        messa.setText(message)
        messa.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messa.exec_()

    def login(self):
        available=0
        if len(self.password_lin.text()) <= 1:                      #If there are no data uwarning box to enter data
            self.warningBox("Error",'Enter Valid Data !')
        else:
            username = self.username_line.text()                    #User entered username
            password = self.password_lin.text()                     #USer entered password
            conn = sqlite3.connect('Covid.db')
            cursor = conn.cursor()
            query = '''select UserName,Password from UserLogin'''
            cursor.execute(query)
            val = cursor.fetchall()                                 #Get all data in a list
            if len(val) >= 1:                                       #If data is available
                for x in val:                                       #From the list of data it will check every row
                    if username in x[0] and password in x[1]:       #If password and username matches
                        available=1                                 #The user is avaialable in User Login table will open user window
                        self.user_window()
                        break
                    else:
                        pass                                    #If data not matched go for other user
            # else:
            #     self.warningBox("Error", "No User Data")      #If the data is empty Give error no data
        if(available==0):                                   #If user is not available in the User database check in admin database
            query = '''select UserName,Password from AdminLogin'''
            cursor.execute(query)
            val = cursor.fetchall()
            conn.close()
            if len(val) >= 1:
                for x in val:
                    if username in x[0] and password in x[1]:
                        available = 1
                        self.admin_window()
                        break
                    else:
                        pass
        if(available==0):                                   #If still user is not availabe give a warning saying the details are wrong.
            self.warningBox("Error", "Wrong details")

        

    def setupUi(self, Login_Form):
        Login_Form.setObjectName("Login_Form")
        Login_Form.resize(800, 600)
        self.user_name = QtWidgets.QLabel(Login_Form)
        self.user_name.setGeometry(QtCore.QRect(300, 80, 101, 31))
        self.user_name.setObjectName("user_name")
        self.password = QtWidgets.QLabel(Login_Form)
        self.password.setGeometry(QtCore.QRect(300, 120, 81, 21))
        self.password.setObjectName("password")
        self.username_line = QtWidgets.QLineEdit(Login_Form)
        self.username_line.setGeometry(QtCore.QRect(370, 90, 113, 22))
        self.username_line.setObjectName("username_line")
        self.password_lin = QtWidgets.QLineEdit(Login_Form)
        self.password_lin.setGeometry(QtCore.QRect(370, 120, 113, 22))
        self.password_lin.setObjectName("password_lin")
        self.password_lin.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button = QtWidgets.QPushButton(Login_Form)
        self.login_button.setGeometry(QtCore.QRect(350, 170, 93, 28))
        self.login_button.setObjectName("login_button")
        self.login_button.clicked.connect(self.login)
        self.login_button.clicked.connect(Login_Form.close)

        self.retranslateUi(Login_Form)
        QtCore.QMetaObject.connectSlotsByName(Login_Form)

    def retranslateUi(self, Login_Form):
        _translate = QtCore.QCoreApplication.translate
        Login_Form.setWindowTitle(_translate("Login_Form", "Login Form"))
        self.user_name.setText(_translate("Login_Form", "UserName"))
        self.password.setText(_translate("Login_Form", "Password"))
        self.login_button.setText(_translate("Login_Form", "Login"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login_Form = QtWidgets.QMainWindow()
    ui = Ui_Login_Form()
    ui.setupUi(Login_Form)
    Login_Form.show()
    sys.exit(app.exec_())
