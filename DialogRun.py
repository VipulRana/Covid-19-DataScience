from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import QInputDialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

#load databases
main_data=pd.read_csv("archive/covid_19_data.csv")
data_2=pd.read_csv('archive/COVID19_line_list_data.csv')
data_2=data_2.drop(columns=['case_in_country', 'Unnamed: 3','Unnamed: 21','Unnamed: 22','Unnamed: 23','Unnamed: 24','Unnamed: 25','Unnamed: 26'])
recovered_table=pd.read_csv('archive/time_series_covid_19_recovered.csv')
us_confirmed=pd.read_csv('archive/time_series_covid_19_confirmed_US.csv')
us_deaths=pd.read_csv('archive/time_series_covid_19_deaths_US.csv')

class Ui_DialogRun(object):

    def show_image(self,DialogRun):
        queries = []
        queries_text=[]
        conn = sqlite3.connect('Covid.db')
        cursor = conn.cursor()
        query = '''select query_title from queries;'''
        cursor.execute(query)
        info = cursor.fetchall()                #list of queries from queries table
        for q in info:
            for x in q:
                queries.append(x)
        query = '''select query_title from queries_text;'''             #list of queries from queries_text table
        cursor.execute(query)
        info2 = cursor.fetchall()
        for q in info2:
            for x in q:
                queries_text.append(x)
        all_queries = queries + queries_text                    #Combined list of all queries
        data = QInputDialog.getItem(DialogRun, "List of Queries", "Query", all_queries)
        name = data[0]
        ok= data[1]
        if ok:
            if(name in queries):
                cursor.execute("select query_title,query from queries where query_title=?;", (name,))           #get the query data related to the name selected by the admin
                info = cursor.fetchall()
                print(info)
                query = info[0][1]              #Store query from database into query
                print(query)
                query_name = name               #query name is the name slected by the admin
                image = query_name + '.png'     #image name we will need is query_name.png
                print(image)
                exec(query)                     #execute the query selected
                self.Image.setPixmap(QtGui.QPixmap(image))      #Set the image generated on the display
                conn.commit()
                conn.close()
            if (name in queries_text):
                loc = {}                        #Create a dictionary
                key = 'result'                  #key value as result
                cursor.execute("select query_title,query from queries_text where query_title=?;", (name,))      #get the query data from the table queries_text  of entered name
                info = cursor.fetchall()
                query = info[0][1]
                exec(query, globals(), loc)             #execute query
                res = loc['result']
                print(res)
                if key in loc.keys():
                    res = loc['result']
                self.Image.setText(res)           #Set display text as res string
                print(" text set")
                conn.commit()
                conn.close()

    def setupUi(self, DialogRun):
        DialogRun.setObjectName("DialogRun")
        DialogRun.resize(689, 530)
        self.Image = QtWidgets.QLabel(DialogRun)                            #Text lable can be also used to display image using pixmap
        self.Image.setGeometry(QtCore.QRect(0, 0, 691, 401))
        self.Image.setScaledContents(True)
        self.Image.setAlignment(QtCore.Qt.AlignCenter)
        self.Image.setObjectName("Image")
        self.pushSelect = QtWidgets.QPushButton(DialogRun)                  #Selct button to get the list of queries
        self.pushSelect.setGeometry(QtCore.QRect(280, 470, 93, 28))
        self.pushSelect.setObjectName("pushSelect")



        self.retranslateUi(DialogRun)
        QtCore.QMetaObject.connectSlotsByName(DialogRun)
        self.pushSelect.clicked.connect(lambda: self.show_image(DialogRun))

    def retranslateUi(self, DialogRun):
        _translate = QtCore.QCoreApplication.translate
        DialogRun.setWindowTitle(_translate("DialogRun", "Dialog"))
        self.Image.setText(_translate("DialogRun", "Result"))
        self.pushSelect.setText(_translate("DialogRun", "Select"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogRun = QtWidgets.QDialog()
    ui = Ui_DialogRun()
    ui.setupUi(DialogRun)
    DialogRun.show()
    sys.exit(app.exec_())
