from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

#Loading required databases
main_data=pd.read_csv("archive/covid_19_data.csv")
data_2=pd.read_csv('archive/COVID19_line_list_data.csv')
data_2=data_2.drop(columns=['case_in_country', 'Unnamed: 3','Unnamed: 21','Unnamed: 22','Unnamed: 23','Unnamed: 24','Unnamed: 25','Unnamed: 26'])
recovered_table=pd.read_csv('archive/time_series_covid_19_recovered.csv')
us_confirmed=pd.read_csv('archive/time_series_covid_19_confirmed_US.csv')
us_deaths=pd.read_csv('archive/time_series_covid_19_deaths_US.csv')

class Ui_AddQueries(object):
    flag=0                              #By defualt flag is set to image
    def isimage(self,seleted):          #If radio butoon is image set flag to 0
        if seleted:
            global flag
            flag=0

    def istext(self,seleted):           #If radio button us text set the flag to 1
        if seleted:
            global flag
            flag=1

    def add_queries(self):
        if flag==1:                     #if flag is text
            loc = {}                    #empty dictionary
            key='result'                #key is result for text
            query_name=self.NameEdit.text()         #Query name given by admin
            query_command=self.CommandEdit.toPlainText()        #Query given by admin
            print(query_command)
            #exec(query_command)
            exec(query_command,globals(),loc)                   #Executing query global used to access variable 'result' of query and store it in dictionary
            print("execexecuted")
            res=loc['result']                                   #Get the value where key is result
            print(res)
            if key in loc.keys():
                res=loc['result']
                conn = sqlite3.connect('Covid.db')
                print("connection made text")
                cursor = conn.cursor()
                create_query_table = '''CREATE TABLE IF NOT EXISTS queries_text
                                (query_title text, query text, res text);'''
                cursor.execute(create_query_table)
                print("print create executed text")
                cursor.execute("INSERT INTO queries_text (query_title,query,res) VALUES (?,?,?)",
                                (query_name, query_command, res))                       #Insert the query name, query and the result text into database
                print("insert executed in text")
                conn.commit()
                conn.close()
                print("committed queries_text")
        else:                           #If option selected is image
            query_name = self.NameEdit.text()               #Query name by admin
            query_command = self.CommandEdit.toPlainText()      #Query entered by admin
            exec(query_command)                             #exec query., since the query will generate image as queryname+'.png'
            print("entered else")
            img=query_name+'.png'                           #The name of the image as a string
            with open(img,'rb') as f:                       #Open the generated image and save it bytes
                image=f.read()
            print("Converted to byte")
            conn=sqlite3.connect('Covid.db')
            print("connection made")
            cursor=conn.cursor()
            create_query_table='''CREATE TABLE IF NOT EXISTS queries
                (query_title text, query text, image BLOB);'''              #BLOB format to save image in database
            cursor.execute(create_query_table)
            print("print create executed")
            cursor.execute("INSERT INTO queries (query_title,query,image) VALUES (?,?,?)", (query_name,query_command,image))            #Insert query name, query and image to the database
            print("insert executed")
            conn.commit()
            conn.close()
            print("committed")

    # def add_queries(self):
    #     loc={}
    #     key='result'
    #     query_name=self.NameEdit.text()
    #     query_command=self.CommandEdit.toPlainText()
    #     print(query_command)
    #     #exec(query_command)
    #     exec(query_command,globals(),loc)
    #     print("execexecuted")
    #     res=loc['result']
    #     print(res)
    #     if key in loc.keys():
    #         res=loc['result']
    #         conn = sqlite3.connect('Covid.db')
    #         print("connection made text")
    #         cursor = conn.cursor()
    #         create_query_table = '''CREATE TABLE IF NOT EXISTS queries_text
    #                          (query_title text, query text, res text);'''
    #         cursor.execute(create_query_table)
    #         print("print create executed text")
    #         cursor.execute("INSERT INTO queries_text (query_title,query,res) VALUES (?,?,?)",
    #                        (query_name, query_command, res))
    #         print("insert executed in text")
    #         conn.commit()
    #         conn.close()
    #         print("committed queries_text")
    #     else:
    #         print("entered else")
    #         img=query_name+'.png'
    #         with open(img,'rb') as f:
    #             image=f.read()
    #         print("Converted to byte")
    #         conn=sqlite3.connect('Covid.db')
    #         print("connection made")
    #         cursor=conn.cursor()
    #         create_query_table='''CREATE TABLE IF NOT EXISTS queries
    #             (query_title text, query text, image BLOB);'''
    #         cursor.execute(create_query_table)
    #         print("print create executed")
    #         cursor.execute("INSERT INTO queries (query_title,query,image) VALUES (?,?,?)", (query_name,query_command,image))
    #         print("insert executed")
    #         conn.commit()
    #         conn.close()
    #         print("committed")

    def setupUi(self, AddQueries):
        AddQueries.setObjectName("AddQueries")
        AddQueries.resize(595, 404)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddQueries)             #button group containing Ok and cancel Button
        self.buttonBox.setGeometry(QtCore.QRect(230, 340, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.labelQueryName = QtWidgets.QLabel(AddQueries)                  #Query name text
        self.labelQueryName.setGeometry(QtCore.QRect(30, 40, 101, 21))
        self.labelQueryName.setAlignment(QtCore.Qt.AlignCenter)
        self.labelQueryName.setObjectName("labelQueryName")
        self.NameEdit = QtWidgets.QLineEdit(AddQueries)                     #Query name input text box
        self.NameEdit.setGeometry(QtCore.QRect(130, 40, 411, 22))
        self.NameEdit.setObjectName("NameEdit")
        self.labelCommand = QtWidgets.QLabel(AddQueries)                    #Query text
        self.labelCommand.setGeometry(QtCore.QRect(10, 80, 111, 20))
        self.labelCommand.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCommand.setObjectName("labelCommand")
        self.CommandEdit = QtWidgets.QTextEdit(AddQueries)                  #Query input text box
        self.CommandEdit.setGeometry(QtCore.QRect(130, 80, 411, 171))
        self.CommandEdit.setObjectName("CommandEdit")
        self.radioButtonText = QtWidgets.QRadioButton(AddQueries)           #radio button for text
        self.radioButtonText.setGeometry(QtCore.QRect(130, 270, 95, 21))
        self.radioButtonText.setObjectName("radioButtonText")
        self.radioButtonImage = QtWidgets.QRadioButton(AddQueries)          #Radio button for image
        self.radioButtonImage.setGeometry(QtCore.QRect(230, 270, 111, 21))
        self.radioButtonImage.setObjectName("radioButtonImage")
        self.note = QtWidgets.QLabel(AddQueries)                            #Note
        self.note.setGeometry(QtCore.QRect(10, 300, 571, 20))
        self.note.setObjectName("note")

        self.retranslateUi(AddQueries)
        self.radioButtonImage.toggled.connect(self.isimage)             #If radio button image is toggled set flag to 0
        self.radioButtonText.toggled.connect(self.istext)               #If radio button text is toggled set flag to 1
        self.buttonBox.accepted.connect(self.add_queries)               #If ok selected add query function
        self.buttonBox.accepted.connect(AddQueries.close)               #Close the window
        self.buttonBox.rejected.connect(AddQueries.reject)
        QtCore.QMetaObject.connectSlotsByName(AddQueries)

    def retranslateUi(self, AddQueries):
        _translate = QtCore.QCoreApplication.translate
        AddQueries.setWindowTitle(_translate("AddQueries", "Dialog"))
        self.labelQueryName.setText(_translate("AddQueries", "Query Name"))
        self.labelCommand.setText(_translate("AddQueries", "Query Command"))
        self.radioButtonText.setText(_translate("AddQueries", "Text Output"))
        self.radioButtonImage.setText(_translate("AddQueries", "Image Output"))
        self.note.setText(_translate("AddQueries","Note: To store the query which will be give an text ouput the ouput must be stored in result variable."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddQueries = QtWidgets.QDialog()
    ui = Ui_AddQueries()
    ui.setupUi(AddQueries)
    AddQueries.show()
    sys.exit(app.exec_())
