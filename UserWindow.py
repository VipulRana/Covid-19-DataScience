from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import QInputDialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

main_data=pd.read_csv("archive/covid_19_data.csv")
data_2=pd.read_csv('archive/COVID19_line_list_data.csv')
data_2=data_2.drop(columns=['case_in_country', 'Unnamed: 3','Unnamed: 21','Unnamed: 22','Unnamed: 23','Unnamed: 24','Unnamed: 25','Unnamed: 26'])
recovered_table=pd.read_csv('archive/time_series_covid_19_recovered.csv')
us_confirmed=pd.read_csv('archive/time_series_covid_19_confirmed_US.csv')
us_deaths=pd.read_csv('archive/time_series_covid_19_deaths_US.csv')

class Ui_UserWindow(object):

    def login_form(self):
        from login import Ui_Login_Form
        self.LoginWindow = QtWidgets.QMainWindow()
        self.ui = Ui_Login_Form()
        self.ui.setupUi(self.LoginWindow)
        self.LoginWindow.show()

    def load_list_data(self,UserWindow):
        items1 = []
        items2 = []
        conn = sqlite3.connect('Covid.db')
        cursor = conn.cursor()
        query = '''select query_title from queries;'''
        cursor.execute(query)
        info = cursor.fetchall()
        for q in info:
            for x in q:
                items1.append(x)
        print(items1)
        query = '''select query_title from queries_text;'''
        cursor.execute(query)
        info2 = cursor.fetchall()
        for q in info2:
            for x in q:
                items2.append(x)
        print(items2)
        all_items = items1 + items2
        data = QInputDialog.getItem(UserWindow, "List of Queries", "Query", all_items)
        name = data[0]
        ok = data[1]  # IF option is selected
        print(name)
        if ok:
            print("ok")
            if (name in items2):
                print("inside text")
                loc = {}
                key = 'result'
                cursor.execute("select query_title,query from queries_text where query_title=?;", (name,))
                info = cursor.fetchall()
                query= info[0][1]
                print(query)
                # exec(query_command)
                exec(query, globals(), loc)
                print("execexecuted")
                res = loc['result']
                print(res)
                if key in loc.keys():
                    res = loc['result']
                self.DisplayLabel.setText(res)
                print(" text set")
                # self.DisplayLabel.adjustSize()
                # UserWindow.adjustSize()
                conn.commit()
                print("text commited")
                conn.close()
            if (name in items1):
                print("inside image")
                cursor.execute("select query_title,query from queries where query_title=?;", (name,))
                info = cursor.fetchall()
                query = info[0][1]
                query_name = name
                image = query_name + '.png'
                print(image)
                exec(query)
                self.DisplayLabel.setPixmap(QtGui.QPixmap(image))
                print("image set")
                conn.commit()
                print("commited")
                conn.close()

    def setupUi(self, UserWindow):
        UserWindow.setObjectName("UserWindow")
        UserWindow.resize(912, 640)
        self.centralwidget = QtWidgets.QWidget(UserWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.DisplayLabel = QtWidgets.QLabel(self.centralwidget)
        self.DisplayLabel.setGeometry(QtCore.QRect(0, 0, 911, 461))
        self.DisplayLabel.setScaledContents(True)
        self.DisplayLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.DisplayLabel.setObjectName("DisplayLabel")
        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(400, 510, 93, 28))
        self.StartButton.setObjectName("StartButton")
        UserWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(UserWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 912, 25))
        self.menubar.setObjectName("menubar")
        self.menuLogout = QtWidgets.QMenu(self.menubar)
        self.menuLogout.setObjectName("menuLogout")
        UserWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(UserWindow)
        self.statusbar.setObjectName("statusbar")
        UserWindow.setStatusBar(self.statusbar)
        self.actionLogout = QtWidgets.QAction(UserWindow)
        self.actionLogout.setObjectName("actionLogout")
        self.menuLogout.addAction(self.actionLogout)
        self.menubar.addAction(self.menuLogout.menuAction())
        print("Main def")

        self.retranslateUi(UserWindow)
        QtCore.QMetaObject.connectSlotsByName(UserWindow)

        print("button clicked")
        self.StartButton.clicked.connect(lambda : self.load_list_data(UserWindow))
        self.actionLogout.triggered.connect(self.login_form)
        self.actionLogout.triggered.connect(UserWindow.close)

    def retranslateUi(self, UserWindow):
        _translate = QtCore.QCoreApplication.translate
        UserWindow.setWindowTitle(_translate("UserWindow", "MainWindow"))
        self.DisplayLabel.setText(_translate("UserWindow", "Select The Query"))
        self.StartButton.setText(_translate("UserWindow", "Start"))
        self.menuLogout.setTitle(_translate("UserWindow", "Logout"))
        self.actionLogout.setText(_translate("UserWindow", "Logout"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UserWindow = QtWidgets.QMainWindow()
    ui = Ui_UserWindow()
    ui.setupUi(UserWindow)
    UserWindow.show()
    sys.exit(app.exec_())
