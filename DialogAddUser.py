from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

class Ui_AddUser(object):
    def messagebox(self,title,message):
        messa=QtWidgets.QMessageBox()
        messa.setWindowTitle(title)
        messa.setText(message)
        messa.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messa.exec_()

    def warningBox(self,title,message):
        messa=QtWidgets.QMessageBox()
        messa.setWindowTitle(title)
        messa.setText(message)
        messa.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messa.exec_()

    def add_user(self):
        username = self.UsernameEdit.text()         #Get username entered by admin
        password = self.PassowordEdit.text()        #Get password enter by admin
        conn = sqlite3.connect('Covid.db')
        cursor = conn.cursor()
        query = '''select UserName,Password from UserLogin'''
        cursor.execute(query)
        val = cursor.fetchall()                    #Get list of all users
        print(val)
        available = 0
        if len(val) >= 1:                           #If the table has data
            for x in val:                           #Check every row
                if username in x[0]:                #If username is available show a message user already esists
                    available +=1
                    print("matched")
                    self.warningBox("Error", "Username already exists!!")
                    break
                else:                               #Check next row
                    print("Looking next")
                    pass
            if(available==0):                       #If user is not available add username and password in user table
                #insert_stmt = '''INSERT INTO UserLogin (UserId,UserName,Password) VALUES (%s,%s,%s),'''
                cursor.execute("INSERT INTO UserLogin (UserName,Password) VALUES (?,?)", (username, password))
                #recordTuple = (high,username,password)
                #cursor.execute(insert_stmt, recordTuple)
                #self.messageBox("Success", "User Created")
                conn.commit()
                conn.close()

        else:                                   #If table is empty there is no user data add the first user
            print("Adding new outside for")
            # sql_comm = '''Insert into UserLogin(UserId,Username,Password) values (003,%s,%s);'''
            # cursor.execute(sql_comm,(username,password))
            cursor.execute("INSERT INTO UserLogin (UserName,Password) VALUES (?,?)", (username, password))
            self.messageBox("Success", "User Created")
            conn.commit()
            conn.close()

    def setupUi(self, AddUser):
        AddUser.setObjectName("AddUser")
        AddUser.resize(402, 195)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddUser)            #Button groups containing OK and Cancel button
        self.buttonBox.setGeometry(QtCore.QRect(30, 130, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.labelUsername = QtWidgets.QLabel(AddUser)                  #USer name Text
        self.labelUsername.setGeometry(QtCore.QRect(30, 40, 101, 21))
        self.labelUsername.setAlignment(QtCore.Qt.AlignCenter)
        self.labelUsername.setObjectName("labelUsername")
        self.UsernameEdit = QtWidgets.QLineEdit(AddUser)                #Username input box
        self.UsernameEdit.setGeometry(QtCore.QRect(130, 40, 113, 22))
        self.UsernameEdit.setObjectName("UsernameEdit")
        self.labelPasowrd = QtWidgets.QLabel(AddUser)                   #User name Password Text
        self.labelPasowrd.setGeometry(QtCore.QRect(30, 80, 91, 20))
        self.labelPasowrd.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPasowrd.setObjectName("labelPasowrd")
        self.PassowordEdit = QtWidgets.QLineEdit(AddUser)               #Password input box
        self.PassowordEdit.setGeometry(QtCore.QRect(130, 80, 113, 22))
        self.PassowordEdit.setObjectName("PassowrdEdit")

        self.retranslateUi(AddUser)
        self.buttonBox.accepted.connect(self.add_user)                  #If ok is selected go to add user
        self.buttonBox.accepted.connect(AddUser.close)                  #And close the widow
        self.buttonBox.rejected.connect(AddUser.reject)
        QtCore.QMetaObject.connectSlotsByName(AddUser)

    def retranslateUi(self, AddUser):
        _translate = QtCore.QCoreApplication.translate
        AddUser.setWindowTitle(_translate("AddUser", "Dialog"))
        self.labelUsername.setText(_translate("AddUser", "Username"))
        self.labelPasowrd.setText(_translate("AddUser", "Password"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddUser = QtWidgets.QDialog()
    ui = Ui_AddUser()
    ui.setupUi(AddUser)
    AddUser.show()
    sys.exit(app.exec_())
