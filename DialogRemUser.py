from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

class Ui_RemoveUser(object):

    def messagebox(self,title,message):
        messa=QtWidgets.QMessageBox()
        messa.setWindowTitle(title)
        messa.setText(message)
        messa.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messa.exec_()

    def load_all_user(self):                                #List all the user's id and username
        conn = sqlite3.connect('Covid.db')
        cursor = conn.cursor()
        queries_data = '''SELECT UserId,UserName from  UserLogin;'''
        cursor.execute(queries_data)
        info = cursor.fetchall()
        print(info)
        row = 0
        self.tableWidget.setRowCount(len(info))
        for data in info:
            # for subdata in data:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(data[0])))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(data[1]))
            row += 1
        conn.close()

    def rem_user(self):
        user_to_remove=self.NameEdit.text()             #Username entered by the admin to be removed
        conn = sqlite3.connect('Covid.db')
        cursor = conn.cursor()
        #rem_query='''DELETE FROM UserLogin WHERE UserName = %s'''
        #cursor.execute(rem_query,remove)
        cursor.execute("DELETE FROM UserLogin WHERE UserName = ?", (user_to_remove,))   #Sql query to delete the user row with the username enter by admin
        conn.commit()
        conn.close()
        self.messagebox("Success","User Deleted")

    def setupUi(self, RemoveUser):
        RemoveUser.setObjectName("RemoveUser")
        RemoveUser.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(RemoveUser)             #Button group with OK and cancel button
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tableWidget = QtWidgets.QTableWidget(RemoveUser)              #Table widget to show user list and id
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 256, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)                                  #Table will contain 2 rows id and username
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)                  #Enter username text
        self.UserLable = QtWidgets.QLabel(RemoveUser)
        self.UserLable.setGeometry(QtCore.QRect(10, 230, 131, 16))
        self.UserLable.setAlignment(QtCore.Qt.AlignCenter)
        self.UserLable.setObjectName("UserLable")
        self.NameEdit = QtWidgets.QLineEdit(RemoveUser)                     #Username input text box
        self.NameEdit.setGeometry(QtCore.QRect(150, 230, 113, 22))
        self.NameEdit.setObjectName("NameEdit")
        self.tableWidget.setColumnWidth(0,100)
        self.tableWidget.setColumnWidth(1,135)
        self.retranslateUi(RemoveUser)

        self.load_all_user()

        self.buttonBox.accepted.connect(self.rem_user)                  #If oK selected remove the user function
        self.buttonBox.accepted.connect(RemoveUser.close)               #Close window
        self.buttonBox.rejected.connect(RemoveUser.reject)
        QtCore.QMetaObject.connectSlotsByName(RemoveUser)

    def retranslateUi(self, RemoveUser):
        _translate = QtCore.QCoreApplication.translate
        RemoveUser.setWindowTitle(_translate("RemoveUser", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("RemoveUser", "UserId"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("RemoveUser", "UserName"))
        self.UserLable.setText(_translate("RemoveUser", "Enter User Name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RemoveUser = QtWidgets.QDialog()
    ui = Ui_RemoveUser()
    ui.setupUi(RemoveUser)
    RemoveUser.show()
    sys.exit(app.exec_())
