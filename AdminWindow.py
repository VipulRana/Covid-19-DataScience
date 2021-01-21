from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import QInputDialog
from DialogAddUser import Ui_AddUser
from DialogAddQueries import Ui_AddQueries
from DialogRemUser import Ui_RemoveUser
from DialogRun import Ui_DialogRun

class Ui_AdminWindow(object):
    def login_form(self):                   #Transfer control to login form
        from login import Ui_Login_Form
        self.LoginWindow = QtWidgets.QMainWindow()
        self.ui = Ui_Login_Form()
        self.ui.setupUi(self.LoginWindow)
        self.LoginWindow.show()

    def del_row(self,AdminWindow):             #Delete selected query
        queries=[]
        queries_text=[]
        conn = sqlite3.connect('Covid.db')
        cursor = conn.cursor()
        query = '''select query_title from queries;'''
        cursor.execute(query)
        info = cursor.fetchall()
        for q in info:
            for x in q:
                queries.append(x)                       #List of queries in queries table(contains image query)
        query = '''select query_title from queries_text;'''
        cursor.execute(query)
        info2 = cursor.fetchall()
        for q in info2:
            for x in q:
                queries_text.append(x)                  #List of queries in queries_text table (contains test output query)
        all_queries=queries + queries_text              #Combines both list
        data = QInputDialog.getItem(AdminWindow, "List of Queries", "Query", all_queries)       #Open a dropwdown dialog
        print(data)
        name = data[0]                                          #Name of query
        ok=data[1]                                              #True or False
        if ok:                                                  #If user has selected any option
            if(name in queries):                                #If the selected query name is from queries list
                cursor.execute("DELETE FROM queries WHERE query_title = ?", (name,))    #Delete query
                conn.commit()
                conn.close()
            if(name in queries_text):                           #If query is from query_text list
                cursor.execute("DELETE FROM queries_text WHERE query_title=?",(name,))  #Delete query
                conn.commit()
                conn.close()

    def fill_table(self):               #Load Tablewidget with the queries data
        conn=sqlite3.connect('Covid.db')
        cursor=conn.cursor()
        queries_data='''SELECT * from  queries;'''
        cursor.execute(queries_data)
        info1=cursor.fetchall()
        queries_data = '''SELECT * from  queries_text;'''
        cursor.execute(queries_data)
        info2 = cursor.fetchall()
        all_list=info1+info2
        row=0
        self.tableWidget.setRowCount(len(all_list))             #Number of rows depend on the list of total queries
        for data in all_list:
            # for subdata in data:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(data[0]))       #Query Name
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(data[1]))       #Query
            row+=1
        conn.close()

    def show_add_query(self):               #Transfer control to add query page
        self.QueryWindow = QtWidgets.QDialog()
        self.ui = Ui_AddQueries()
        self.ui.setupUi(self.QueryWindow)
        self.QueryWindow.show()

    def show_add_dialog(self):              #Transfer control to add user dialog page
        self.AddDialogWindow = QtWidgets.QDialog()
        self.ui = Ui_AddUser()
        self.ui.setupUi(self.AddDialogWindow)
        self.AddDialogWindow.show()

    def show_rem_dialog(self):              #Transfer control to remove user page
        self.RemDialogWindow = QtWidgets.QDialog()
        self.ui = Ui_RemoveUser()
        self.ui.setupUi(self.RemDialogWindow)
        self.RemDialogWindow.show()

    def run_query(self):                    #Transfer control to run query page
        self.DialogRunWindow = QtWidgets.QDialog()
        self.ui = Ui_DialogRun()
        self.ui.setupUi(self.DialogRunWindow)
        self.DialogRunWindow.show()

    def setupUi(self, AdminWindow):
        AdminWindow.setObjectName("AdminWindow")
        AdminWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(AdminWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Welcomelabel = QtWidgets.QLabel(self.centralwidget)            #Welcome message
        self.Welcomelabel.setGeometry(QtCore.QRect(160, 30, 451, 61))
        self.Welcomelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Welcomelabel.setObjectName("Welcomelabel")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)       #Table to list data
        self.tableWidget.setGeometry(QtCore.QRect(75, 140, 651, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)                                  #@ rows 1 for name and 1 for query
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.pushAdd = QtWidgets.QPushButton(self.centralwidget)            #Add button
        self.pushAdd.setGeometry(QtCore.QRect(150, 350, 93, 28))
        self.pushAdd.setObjectName("pushAdd")
        self.pushRun = QtWidgets.QPushButton(self.centralwidget)            #Run button
        self.pushRun.setGeometry(QtCore.QRect(340, 350, 93, 28))
        self.pushRun.setObjectName("pushRun")
        self.pushDelete = QtWidgets.QPushButton(self.centralwidget)         #Delete Button
        self.pushDelete.setGeometry(QtCore.QRect(530, 350, 93, 28))
        self.pushDelete.setObjectName("pushDelete")
        self.pushRefresh = QtWidgets.QPushButton(self.centralwidget)        #Refersh Button
        self.pushRefresh.setGeometry(QtCore.QRect(690, 510, 93, 28))
        self.pushRefresh.setObjectName("pushRefresh")
        AdminWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AdminWindow)                      #Menu Bar with logout and Add user actions
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        self.menuLogout = QtWidgets.QMenu(self.menubar)                     #Logout button
        self.menuLogout.setObjectName("menuLogout")
        self.menuAdd_User = QtWidgets.QMenu(self.menubar)                   #Add User button
        self.menuAdd_User.setObjectName("menuAdd_User")
        AdminWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AdminWindow)
        self.statusbar.setObjectName("statusbar")
        AdminWindow.setStatusBar(self.statusbar)
        self.actionAdd_User = QtWidgets.QAction(AdminWindow)
        self.actionAdd_User.setObjectName("actionAdd_User")
        self.actionRemove_User = QtWidgets.QAction(AdminWindow)
        self.actionRemove_User.setObjectName("actionRemove_User")
        self.menuAdd_User.addAction(self.actionAdd_User)
        self.menuAdd_User.addAction(self.actionRemove_User)
        self.actionLogout = QtWidgets.QAction(AdminWindow)
        self.actionLogout.setObjectName("actionLogout")
        self.menuLogout.addAction(self.actionLogout)
        self.menubar.addAction(self.menuLogout.menuAction())
        self.menubar.addAction(self.menuAdd_User.menuAction())
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,550)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 40, 201, 111))

        self.fill_table()

        # Keeping the text of label empty initially.
        self.retranslateUi(AdminWindow)
        QtCore.QMetaObject.connectSlotsByName(AdminWindow)

        self.pushAdd.clicked.connect(self.show_add_query)
        self.pushDelete.clicked.connect(lambda: self.del_row(AdminWindow))
        self.pushRefresh.clicked.connect(self.fill_table)
        self.pushRun.clicked.connect(self.run_query)
        self.actionAdd_User.triggered.connect(self.show_add_dialog)
        self.actionRemove_User.triggered.connect(self.show_rem_dialog)
        self.actionLogout.triggered.connect(self.login_form)
        self.actionLogout.triggered.connect(AdminWindow.close)

    def retranslateUi(self, AdminWindow):
        _translate = QtCore.QCoreApplication.translate
        AdminWindow.setWindowTitle(_translate("AdminWindow", "MainWindow"))
        self.Welcomelabel.setText(_translate("AdminWindow", "Welcome Admin User"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("AdminWindow", "Query Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("AdminWindow", "Query Command"))
        self.pushAdd.setText(_translate("AdminWindow", "Add"))
        self.pushRun.setText(_translate("AdminWindow", "Run"))
        self.pushDelete.setText(_translate("AdminWindow", "Delete"))
        self.pushRefresh.setText(_translate("AdminWindow", "Refresh Table"))
        self.menuLogout.setStatusTip(_translate("AdminWindow", "Logout Admin"))
        self.menuLogout.setTitle(_translate("AdminWindow", "Logout"))
        self.menuAdd_User.setTitle(_translate("AdminWindow", "User Commands"))
        self.actionAdd_User.setText(_translate("AdminWindow", "Add User"))
        self.actionAdd_User.setStatusTip(_translate("AdminWindow", "Add user Account"))
        self.actionRemove_User.setText(_translate("AdminWindow", "Remove User"))
        self.actionRemove_User.setStatusTip(_translate("AdminWindow", "Remove User Account"))
        self.actionLogout.setText(_translate("AdminWindow", "Logout"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AdminWindow = QtWidgets.QMainWindow()
    ui = Ui_AdminWindow()
    ui.setupUi(AdminWindow)
    AdminWindow.show()
    sys.exit(app.exec_())
