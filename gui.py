###
#    Created by Anh Tu Nguyen/anhtu91@gmail.com
#    Supervisor Rasit Özgüc/rasit.oezguec@umsicht.fraunhofer.de
#    
#    (C) Copyright @Fraunhofer UMSICHT
#    Contents and presentations are protected world-wide.
#    Any kind of using, copying etc. is prohibited without prior permission.
#    All rights - incl. industrial property rights - are reserved.
###

import os
import sys
import shutil
import webbrowser

import re

import mysql.connector
from mysql.connector import Error

import socket
from ftplib import FTP  
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QSizePolicy, QStyledItemDelegate, QFileDialog
from PyQt5.QtCore import Qt, QUrl, QRegExp
from PyQt5.QtGui import QIcon, QRegExpValidator

from dateutil.parser import parse
from datetime import datetime, date
from database import uiDatabaseWindow


#Change these lines for appropriate MySql server
databaseTable = "intentar_chemicals_new"
database = "test4fraunhofer"
databasePassword = "Thaivannhan59@"
databaseUser = "newuser"
databaseLocalhost = "localhost"

#FTP Server config
userFTPServer = "fraunhoferumsicht"
passwordFTPServer = "password@Datenbank"
portFTPServer = 1026

#Save setting and datasheet folder
saveLastIPAddressFile = "setting"
securityDataSheetFolderPath = "/security_datasheet"
currentRunningFolder = str(os.path.dirname(os.path.abspath(__file__)))

#Config display columns in table
columnsList = ['No.', 'Chemikalienbezeichnung', 'Schrank', 'CAS-Nummer', 'Lieferant', 'g\ml', 'Stückzahl', 'Zuständig', 'Sicherheitsdatenblatt','Datum', 'H-Sätze']
columns = len(columnsList) #Number of columns in database table/ Change when add more columns

#Config the order of columns in table
noCol = 0
nameChemicalsCol = 1
cabinetsCol = 2
casNumberCol = 3
supplierCol = 4
quantityCol = 5
quantityAmountCol = 6
personCol = 7
securityDataCol = 8
dateCol = 9
commentCol = 10

#Config columns width 
noColWidth = 50
nameChemicalsColWidth = 390
cabinetsColWidth = 200
casNumberColWidth = 150
supplierColWidth = 150
quantityColWidth = 100
quantityAmountColWidth = 100
personColWidth = 180
securityColWidth = 500
dateColWidth = 150
commentColWidth = 315

#Change this list item to change marking red in table
redMarkingCommentList = ["300", "310", "330", "301", "311", "331", "340", "350", "360", "370", "372"]

#Config cabinnets. Change this list may cause errors in table. To fix error runs import export programm again to overwrite/update cabinnet list!
cabinnetsList = [
    "CL25_Chem",
    "CL25_Gefahrstoff",
    "CL25_Gift",
    "CL22_Chem"
]
cabinnetsListExtend = cabinnetsList.copy()
cabinnetsListExtend.insert(0,"Alle")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(988, 733)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 167, 901, 401))
        self.layoutWidget.setObjectName("layoutWidget")
        self.DataLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.DataLayout.setContentsMargins(0, 0, 0, 0)
        self.DataLayout.setObjectName("DataLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbNo = QtWidgets.QLabel(self.layoutWidget)
        self.lbNo.setObjectName("lbNo")
        self.verticalLayout_2.addWidget(self.lbNo)
        self.lbNameOfChemicals = QtWidgets.QLabel(self.layoutWidget)
        self.lbNameOfChemicals.setObjectName("lbNameOfChemicals")
        self.verticalLayout_2.addWidget(self.lbNameOfChemicals)
        self.lbCabinets = QtWidgets.QLabel(self.layoutWidget)
        self.lbCabinets.setObjectName("lbCabinets")
        self.verticalLayout_2.addWidget(self.lbCabinets)
        self.lbCASNumber = QtWidgets.QLabel(self.layoutWidget)
        self.lbCASNumber.setObjectName("lbCASNumber")
        self.verticalLayout_2.addWidget(self.lbCASNumber)
        self.lbSupplier = QtWidgets.QLabel(self.layoutWidget)
        self.lbSupplier.setObjectName("lbSupplier")
        self.verticalLayout_2.addWidget(self.lbSupplier)
        self.lbQuantity = QtWidgets.QLabel(self.layoutWidget)
        self.lbQuantity.setObjectName("lbQuantity")
        self.verticalLayout_2.addWidget(self.lbQuantity)
        self.lbQuantityNumber = QtWidgets.QLabel(self.layoutWidget)
        self.lbQuantityNumber.setObjectName("lbQuantityNumber")
        self.verticalLayout_2.addWidget(self.lbQuantityNumber)
        self.lbPerson = QtWidgets.QLabel(self.layoutWidget)
        self.lbPerson.setObjectName("lbPerson")
        self.verticalLayout_2.addWidget(self.lbPerson)
        self.lbDatasheet = QtWidgets.QLabel(self.layoutWidget)
        self.lbDatasheet.setObjectName("lbDatasheet")
        self.verticalLayout_2.addWidget(self.lbDatasheet)
        self.lbDate = QtWidgets.QLabel(self.layoutWidget)
        self.lbDate.setObjectName("lbDate")
        self.verticalLayout_2.addWidget(self.lbDate)
        self.lbComment = QtWidgets.QLabel(self.layoutWidget)
        self.lbComment.setObjectName("lbComment")
        self.verticalLayout_2.addWidget(self.lbComment)
        self.DataLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.sbNo = QtWidgets.QSpinBox(self.layoutWidget)
        self.sbNo.setMaximum(9999)
        self.sbNo.setObjectName("sbNo")
        self.verticalLayout.addWidget(self.sbNo)
        self.leNameOfChemicals = QtWidgets.QLineEdit(self.layoutWidget)
        self.leNameOfChemicals.setObjectName("leNameOfChemicals")
        self.verticalLayout.addWidget(self.leNameOfChemicals)
        self.cbCabinets = QtWidgets.QComboBox(self.layoutWidget)
        self.cbCabinets.setObjectName("cbCabinets")
        self.verticalLayout.addWidget(self.cbCabinets)
        self.leCASNumber = QtWidgets.QLineEdit(self.layoutWidget)
        self.leCASNumber.setObjectName("leCASNumber")
        self.verticalLayout.addWidget(self.leCASNumber)
        self.leSupplier = QtWidgets.QLineEdit(self.layoutWidget)
        self.leSupplier.setObjectName("leSupplier")
        self.verticalLayout.addWidget(self.leSupplier)
        self.leQuantity = QtWidgets.QLineEdit(self.layoutWidget)
        self.leQuantity.setObjectName("leQuantity")
        self.verticalLayout.addWidget(self.leQuantity)
        self.sbQuantityNumber = QtWidgets.QSpinBox(self.layoutWidget)
        self.sbQuantityNumber.setMaximum(99999)
        self.sbQuantityNumber.setObjectName("sbQuantityNumber")
        self.verticalLayout.addWidget(self.sbQuantityNumber)
        self.lePerson = QtWidgets.QLineEdit(self.layoutWidget)
        self.lePerson.setObjectName("lePerson")
        self.verticalLayout.addWidget(self.lePerson)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.leSecurity = QtWidgets.QLineEdit(self.layoutWidget)
        self.leSecurity.setObjectName("leSecurity")
        self.horizontalLayout_2.addWidget(self.leSecurity)
        self.btnBrowser = QtWidgets.QPushButton(self.layoutWidget)
        self.btnBrowser.setObjectName("btnBrowser")
        self.horizontalLayout_2.addWidget(self.btnBrowser)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.dateEdit = QtWidgets.QDateEdit(self.layoutWidget)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QtCore.QDate(2020, 1, 1))
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout.addWidget(self.dateEdit)
        self.leComment = QtWidgets.QLineEdit(self.layoutWidget)
        self.leComment.setObjectName("leComment")
        self.verticalLayout.addWidget(self.leComment)
        self.DataLayout.addLayout(self.verticalLayout)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(110, 660, 740, 49))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.ButtonLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.ButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.ButtonLayout.setObjectName("ButtonLayout")
        self.btnSave = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnSave.setFont(font)
        self.btnSave.setObjectName("btnSave")
        self.ButtonLayout.addWidget(self.btnSave)
        self.btnShow = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnShow.setFont(font)
        self.btnShow.setObjectName("btnShow")
        self.ButtonLayout.addWidget(self.btnShow)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(46, 11, 888, 140))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbFraunhoferIcon = QtWidgets.QLabel(self.layoutWidget2)
        self.lbFraunhoferIcon.setText("")
        self.lbFraunhoferIcon.setPixmap(QtGui.QPixmap(os.path.dirname(os.path.abspath(__file__))+"/icon/fraunhofer_icon.jpg"))
        self.lbFraunhoferIcon.setObjectName("lbFraunhoferIcon")
        self.horizontalLayout.addWidget(self.lbFraunhoferIcon)
        self.lbContact = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbContact.setFont(font)
        self.lbContact.setObjectName("lbContact")
        self.horizontalLayout.addWidget(self.lbContact)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(41, 580, 901, 71))
        self.widget.setObjectName("widget")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lbMasterSlaveOffline = QtWidgets.QLabel(self.widget)
        self.lbMasterSlaveOffline.setObjectName("lbMasterSlaveOffline")
        self.horizontalLayout_4.addWidget(self.lbMasterSlaveOffline)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.rbMaster = QtWidgets.QRadioButton(self.widget)
        self.rbMaster.setObjectName("rbMaster")
        self.horizontalLayout_3.addWidget(self.rbMaster)
        self.rbSlave = QtWidgets.QRadioButton(self.widget)
        self.rbSlave.setObjectName("rbSlave")
        self.horizontalLayout_3.addWidget(self.rbSlave)
        self.rbOffline = QtWidgets.QRadioButton(self.widget)
        self.rbOffline.setObjectName("rbOffline")
        self.horizontalLayout_3.addWidget(self.rbOffline)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lbIPAddress = QtWidgets.QLabel(self.widget)
        self.lbIPAddress.setObjectName("lbIPAddress")
        self.verticalLayout_5.addWidget(self.lbIPAddress)
        self.lbConnectionToDatabase = QtWidgets.QLabel(self.widget)
        self.lbConnectionToDatabase.setObjectName("lbConnectionToDatabase")
        self.verticalLayout_5.addWidget(self.lbConnectionToDatabase)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.leIPAddress = QtWidgets.QLineEdit(self.widget)
        self.leIPAddress.setObjectName("leIPAddress")
        self.horizontalLayout_8.addWidget(self.leIPAddress)
        self.btnConnect = QtWidgets.QPushButton(self.widget)
        self.btnConnect.setObjectName("btnConnect")
        self.horizontalLayout_8.addWidget(self.btnConnect)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.lbConnect = QtWidgets.QLabel(self.widget)
        self.lbConnect.setText("")
        self.lbConnect.setPixmap(QtGui.QPixmap(os.path.dirname(os.path.abspath(__file__))+"/icon/not-ok.png"))
        self.lbConnect.setObjectName("lbConnect")
        self.verticalLayout_4.addWidget(self.lbConnect)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 988, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Safe List of Chemicals Batterielabor CL25"))
        self.lbNo.setText(_translate("MainWindow", "No."))
        self.lbNameOfChemicals.setText(_translate("MainWindow", "Name von Chemicals"))
        self.lbCabinets.setText(_translate("MainWindow", "Schrank"))
        self.lbCASNumber.setText(_translate("MainWindow", "CAS-Number"))
        self.lbSupplier.setText(_translate("MainWindow", "Supplier"))
        self.lbQuantity.setText(_translate("MainWindow", "Menge (gram oder mili)"))
        self.lbQuantityNumber.setText(_translate("MainWindow", "Stückzahl"))
        self.lbPerson.setText(_translate("MainWindow", "Zuständig"))
        self.lbDatasheet.setText(_translate("MainWindow", "Sicherheitdatei"))
        self.lbDate.setText(_translate("MainWindow", "Datum"))
        self.lbComment.setText(_translate("MainWindow", "H Sätze"))
        self.btnBrowser.setText(_translate("MainWindow", "       Browser    "))
        self.dateEdit.setDisplayFormat(_translate("MainWindow", "dd.MM.yyyy"))
        self.btnSave.setText(_translate("MainWindow", "Speichern in Datenbank"))
        self.btnShow.setText(_translate("MainWindow", "Datenbank anzeigen"))
        self.lbContact.setText(_translate("MainWindow", "Raumkoordinator: Rasit Özgüc\n"
"Durchwahl: -1141\n"
"E-Mail: rasit.oezguec@umsicht.fraunhofer.de"))
        self.lbMasterSlaveOffline.setText(_translate("MainWindow", "Betriebsart     "))
        self.rbMaster.setText(_translate("MainWindow", "Master"))
        self.rbSlave.setText(_translate("MainWindow", "Slave"))
        self.rbOffline.setText(_translate("MainWindow", "Offline"))
        self.lbIPAddress.setText(_translate("MainWindow", "IP Adress von Master"))
        self.lbConnectionToDatabase.setText(_translate("MainWindow", "Verbindung mit Datenbank"))
        self.btnConnect.setText(_translate("MainWindow", "Verbinden"))


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    counterClickedHeader = 0
    databaseHost = ""

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.cbCabinets.addItems(cabinnetsList)
        today = date.today()
        self.dateEdit.setDate(today)
        self.leSecurity.setDisabled(True)
       
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])" 
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.leIPAddress.setValidator(ipValidator)
        
        self.readLastIpAddress()
        self.leIPAddress.setDisabled(True)
        self.btnConnect.setDisabled(True)

        self.rbMaster.clicked.connect(self.clickedRadioBoxMaster)
        self.rbSlave.clicked.connect(self.clickedRadioBoxSlave)
        self.rbOffline.clicked.connect(self.clickedRadioBoxOffline)
        self.btnConnect.clicked.connect(self.updateIPAddressServer)
        self.btnSave.clicked.connect(self.saveButtonClick)
        self.btnShow.clicked.connect(self.showButtonClick)
        self.btnBrowser.clicked.connect(self.browserButtonClick)

    def clickedRadioBoxMaster(self):
        self.leIPAddress.setEnabled(False)
        self.btnConnect.setEnabled(False)
        #if self.window.show:
        #    self.window.close()
        self.databaseHost = self.getCurrentIP()
        self.displayLastNoInDatabase()

    def clickedRadioBoxOffline(self):
        self.leIPAddress.setEnabled(False)
        self.btnConnect.setEnabled(False)
        #if self.window.show:
        #    self.window.close()
        self.databaseHost = databaseLocalhost
        self.displayLastNoInDatabase()

    def clickedRadioBoxSlave(self):
        self.leIPAddress.setEnabled(True)
        self.btnConnect.setEnabled(True)
        self.lbConnect.setPixmap(QtGui.QPixmap(os.path.dirname(os.path.abspath(__file__))+"/icon/not-ok.png"))

    def readLastIpAddress(self):
        saveLastIPFilePath = currentRunningFolder+"/"+saveLastIPAddressFile
        if(os.path.isfile(saveLastIPFilePath) is True):
            lastIpFile = open(saveLastIPFilePath, "r")
            lastIP = lastIpFile.read()
            if(self.isStringIPAddress(lastIP)):
                self.leIPAddress.setText(lastIP)
            lastIpFile.close()

    def isStringIPAddress(self, ipAddress):
        regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
        if(re.search(regex, ipAddress)):  
           return True  
        else:  
            return False

    def updateIPAddressServer(self):
        self.databaseHost = self.leIPAddress.text()

        saveLastIPFilePath = currentRunningFolder+"/"+saveLastIPAddressFile
        if(os.path.isfile(saveLastIPFilePath) is True):
            lastIpFile = open(saveLastIPFilePath, "w+")
            lastIP = lastIpFile.read()
            if(lastIP != self.databaseHost):
                lastIpFile.write(self.databaseHost)

        self.displayLastNoInDatabase()
        
    def displayLastNoInDatabase(self):
        try:
            connection = mysql.connector.connect(host=self.databaseHost,
                                                    database=database,
                                                    user=databaseUser,
                                                    password=databasePassword)
            sql = "select no from "+databaseTable+" order by no DESC LIMIT 1"
            cursor = connection.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()

            if(len(records) != 0):    
                lastNo = records[0][0]
                self.sbNo.setValue(lastNo+1)
            
            self.lbConnect.setPixmap(QtGui.QPixmap(os.path.dirname(os.path.abspath(__file__))+"/icon/ok.png"))
        except mysql.connector.Error as err:
            self.showMessage(QMessageBox.Critical, "Fehler...", "Fehler "+str(err), "Fehler ")
            self.lbConnect.setPixmap(QtGui.QPixmap(os.path.dirname(os.path.abspath(__file__))+"/icon/not-ok.png"))
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()

    def showMessage(self, icon, strText, strInfoText, strTitle):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(strText)
        msg.setInformativeText(strInfoText)
        msg.setWindowTitle(strTitle)
        msg.exec_()

    def isMoreNoExist(self, rows, no):
        noExistList = []
        #Check no. in table
        for row in range(rows):
            noInTable = self.ui.tableWidget.item(row, noCol).text()
            if(noInTable == no): 
                noExistList.append(row+1)
        return noExistList 

    def is_date(self, string, fuzzy=False):
        try: 
            parse(string, fuzzy=fuzzy)
            return True
        except ValueError:
            return False

    def browserButtonClick(self):
        try:
            filename = QFileDialog.getOpenFileName(self, "Datei auswählen",filter="Datei (*.pdf)", options=QFileDialog.DontUseNativeDialog)
            path = filename[0]
            self.leSecurity.setText(path)
        except Exception as e:
            self.showMessage(QMessageBox.Critical, "Fehler...", str(e), "Fehler ")

    def closeDatabaseWindow(self):
        if self.window.show:
            self.window.close()
            self.creatingTables()
            self.window.show()

    def insertDataNoNotExist(self, no, nameOfChemicals, cabinets, casNumber, supplier, quantity, quantityNumber, person, securityData, input_date, comment, mycursor, connection):
        sql = "insert into "+databaseTable+" (no, name_of_chemicals, cabinets, cas_number, supplier, quantity, quantity_number, person, securitydata, input_date, comment) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (no, nameOfChemicals, cabinets, casNumber, supplier, quantity, quantityNumber, person, securityData, input_date, comment)
        mycursor.execute(sql, val)
        connection.commit()
        self.showMessage(QMessageBox.Information, "Fertig!", "Erfolgreich aktuallisiert", "Infos")
        self.closeDatabaseWindow()

    def overwriteDataNoExist(self, no, nameOfChemicals, cabinets, casNumber, supplier, quantity, quantityNumber, person, securityData, input_date, comment, mycursor, connection):
        updateSql = "update "+databaseTable+" set name_of_chemicals ='"+nameOfChemicals+"' ,cabinets = '"+cabinets+"', cas_number = '"+str(casNumber)+"', supplier = '"+str(supplier)+"', quantity = '"+str(quantity)+"', quantity_number = '"+str(quantityNumber)+"', person = '"+person+"' , securitydata = '"+securityData+"' , input_date = '"+str(input_date)+"', comment = '"+comment+"' where no="+str(no)
        mycursor.execute(updateSql)
        connection.commit()
        self.showMessage(QMessageBox.Information, "Fertig!", "Erfolgreich aktuallisiert", "Infos")
        self.closeDatabaseWindow()

    def saveToDatabase(self, no, nameOfChemicals, cabinets, casNumber, supplier, quantity, quantityNumber, person, securityData, input_date, comment):
        try:
            connection = mysql.connector.connect(host=self.databaseHost,
                                                database=database,
                                                user=databaseUser,
                                                password=databasePassword)

            if connection.is_connected():
                mycursor = connection.cursor(buffered=True)

                #Check if No. already exist
                findNoSql = "select * from "+databaseTable+" where no='"+str(no)+"'"
                mycursor.execute(findNoSql)
                rows = mycursor.rowcount

                if rows != 0: #No. exist in data table => Ask overwrite or not
                    reply = QtWidgets.QMessageBox.warning(
                                                    self, "WARNING!",
                                                    "No. existiert schon!\n\n"
                                                    "Wollen Sie wirklich ÜBERSCHREIBEN?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.No)
                    if reply == QtWidgets.QMessageBox.Yes: #Overwrite
                       self.overwriteDataNoExist(no, nameOfChemicals, cabinets, casNumber, supplier, quantity, quantityNumber, person, securityData, input_date, comment, mycursor, connection)
                else: #No. doesn't exists in data table
                    self.insertDataNoNotExist(no, nameOfChemicals, cabinets, casNumber, supplier, quantity, quantityNumber, person, securityData, input_date, comment, mycursor, connection)
                                        
                self.sbNo.setValue(no+1)
        except mysql.connector.Error as err:
            self.showMessage(QMessageBox.Critical, "Fehler...", "Fehler "+str(err), "Fehler ")
        finally:
            if (connection.is_connected()):
                mycursor.close()
                connection.close()   

    def uploadDatasheetToServer(self, fileName, securityDataPath):
        try:
            ftp = FTP()  
            ftp.connect(self.databaseHost, portFTPServer)
            ftp.login(userFTPServer, passwordFTPServer)  

            filelist = [] #to store all files
            ftp.retrlines('NLST',filelist.append) #save all file name to list

            if(fileName not in filelist):
                with open(securityDataPath, 'rb') as f:  #Upload file
                    ftp.storbinary('STOR %s' % fileName, f)  
            ftp.quit()
        except Exception as e:
            errorCode = ""
            if(str(e) in "[Errno 111] Connection refused"):
                errorCode = "FTP Server in Master ist noch nicht gestartet."
            else:
                errorCode = str(e)
            self.showMessage(QMessageBox.Critical, "Fehler wenn datenblatt hochgeladen auf den Master", errorCode, "Fehler ")

    def checkSecurityDatasheetAndCopy(self, securityData):
        if(securityData != ""):
            url = QUrl.fromLocalFile(securityData)
            fileName = ""
            
            if(url.fileName().endswith(".PDF")):
                fileName = url.fileName()[:-4] + ".pdf"      
            else:
                fileName = url.fileName()
                
            #Save local folder    
            securityDataPath = currentRunningFolder+securityDataSheetFolderPath+"/"+fileName

            #Copy file to local save folder
            shutil.copy2(securityData, securityDataPath)
                
            #Check current programm runs in master/slave
            if(self.isCurrentComputerMasterSlave() is False): #Slave => Run upload
                self.uploadDatasheetToServer(fileName, securityDataPath)
                
            return fileName[:-4]

    def saveButtonClick(self):
        #Get input value
        no = self.sbNo.value()
        nameOfChemicals = self.leNameOfChemicals.text()
        casNumber = self.leCASNumber.text()
        supplier = self.leSupplier.text()
        quantity = self.leQuantity.text()
        quantityNumber = self.sbQuantityNumber.value()
        cabinets = self.cbCabinets.currentText()
        person = self.lePerson.text()
        securityData = self.leSecurity.text()

        try:
            #Check security datasheet and copy to save folder
            securityData = self.checkSecurityDatasheetAndCopy(securityData)
        except Exception as e:
            if(str(e) in "are the same file"):
                print(securityData)

        if(securityData is None):
            securityData = ""

        input_date = datetime.strftime(self.dateEdit.date().toPyDate(), '%Y-%m-%d')
        comment = self.leComment.text()

        if no == '':
            self.showMessage(QMessageBox.Critical, "Fehler...", "No. darf nicht leer sein!", "Fehler ")
        else:
            if nameOfChemicals == '':
                self.showMessage(QMessageBox.Critical, "Fehler...", "Name von Chemikals darf nicht leer!", "Fehler ")
            else:
                if quantity == '':
                    self.showMessage(QMessageBox.Critical, "Fehler...", "Menge (gram oder mili) darf nicht leer!", "Fehler ")
                else:
                    if quantityNumber == '':
                        self.showMessage(QMessageBox.Critical, "Fehler...", "Stückzahl darf nicht leer!", "Fehler ")
                    else:
                        if person == '':
                            self.showMessage(QMessageBox.Critical, "Fehler...", "Zuständig darf nicht leer!", "Fehler ")
                        else:                        
                            self.saveToDatabase(no, nameOfChemicals, cabinets, casNumber, supplier, quantity, quantityNumber, person, securityData, input_date, comment)

    def changedCommentSetColor(self, row, col):
        if(col == commentCol):
            newComment = self.ui.tableWidget.item(row, col).text()
            self.setBackgroundColorForCommentRow(row, newComment)

    def importSecurtiyData(self, row, col):
        if(col == securityDataCol):
            try:
                filename = QFileDialog.getOpenFileName(self, "Datei auswählen",filter="Datei (*.pdf)", options=QFileDialog.DontUseNativeDialog)
                path = filename[0]

                if(path != ""):
                    url = QUrl.fromLocalFile(path)
                    securityDataPath = ""

                    #Check if security datasheet already exists in local save folder
                    if(os.path.isfile(currentRunningFolder+securityDataSheetFolderPath+"/"+url.fileName())):
                        securityDataPath = currentRunningFolder+securityDataSheetFolderPath+"/"+url.fileName()
                    else:
                        #Copy file to local save folder
                        shutil.copy2(path, currentRunningFolder+securityDataSheetFolderPath)
                        #Save local folder
                        securityDataPath = currentRunningFolder+securityDataSheetFolderPath+"/"+url.fileName()

                        #Check current programm runs in master/slave
                        if(self.isCurrentComputerMasterSlave() is False): #Slave => Upload datasheet to server
                            self.uploadDatasheetToServer(url.fileName(), securityDataPath)
                        
                    self.setDatasheetRow(row, securityDataPath, False)
            except Exception as e:
                self.showMessage(QMessageBox.Critical, "Fehler...", str(e), "Fehler ")

    def getCurrentIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def isCurrentComputerMasterSlave(self): #return True if master/offline mode activate, False if slave mode activates
        isMasterSlaveOffline = False
        if(self.rbMaster.isChecked() is True):
            isMasterSlaveOffline = True
        elif(self.rbOffline.isChecked() is True):
            isMasterSlaveOffline = True
        elif(self.rbSlave.isChecked() is True):
            isMasterSlaveOffline = False
        return isMasterSlaveOffline

    def downloadDatasheetFromMaster(self, fileName, filePath):
        try:
            ftp = FTP()  
            ftp.connect(self.databaseHost, portFTPServer)
            ftp.login(userFTPServer, passwordFTPServer)  

            filelist = [] #to store all files
            ftp.retrlines('NLST',filelist.append) #save all file name to list

            if(fileName in filelist):
                with open(filePath, "wb") as file:
                    # use FTP's RETR command to download the file
                    ftp.retrbinary(f"RETR {fileName}", file.write)
                ftp.quit()
                return True
            else:
                ftp.quit()
                return False
        except Exception as e:
            errorCode = ""
            if(str(e) in "[Errno 111] Connection refused"):
                errorCode = "FTP Server in Master ist noch nicht gestartet."
            else:
                errorCode = str(e)
            self.showMessage(QMessageBox.Critical, "Fehler wenn datenblatt heruntergeladen von Master", errorCode, "Fehler ")
            return False

    def clickedDatasheetColumn(self, row, col):
        if(col == securityDataCol):
            fileName = self.ui.tableWidget.item(row, col).text()
            if(fileName != ""):
                box = QtWidgets.QMessageBox()
                box.setIcon(QtWidgets.QMessageBox.Question)
                box.setWindowTitle('Info')
                box.setText('Wollen Sie das Datenblatt angucken oder ändern?')
                box.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No|QtWidgets.QMessageBox.Cancel)
                buttonOpen = box.button(QtWidgets.QMessageBox.Yes)
                buttonOpen.setText('Angucken')
                buttonChange = box.button(QtWidgets.QMessageBox.No)
                buttonChange.setText('Ändern')
                box.exec_()

                if box.clickedButton() == buttonOpen: #Add new data
                    securityFilePath = currentRunningFolder+securityDataSheetFolderPath+"/"+fileName+".pdf".lower()
                    if(securityFilePath != ""):
                        downloadSuccessful = False 

                        #Check if security datasheet already exists in local save folder
                        if(os.path.isfile(securityFilePath) is False): 
                            #Check current computer is master or slave
                            if(self.isCurrentComputerMasterSlave() is True): #Master/Offline => Print error
                                self.showMessage(QMessageBox.Critical, "Fehler...", "Gespeicherte Sicherheitsdatei unter dem Ordner wurde gelöscht!", "Fehler ")
                                return
                            else: #Slave => download datasheet from master
                                downloadSuccessful = self.downloadDatasheetFromMaster(fileName+".pdf", securityFilePath)
                                if(downloadSuccessful is False):
                                    self.showMessage(QMessageBox.Critical, "Fehler...", "Gespeicherte Sicherheitsdatei unter dem Ordner wurde in beide Master&Slave gelöscht!", "Fehler ")
                                    return

                        if(downloadSuccessful is True or os.path.isfile(securityFilePath) is True):
                            #Use webbrowser to open pdf data
                            try:
                                webbrowser.open(securityFilePath)
                            except Exception as e:
                                self.showMessage(QMessageBox.Critical, "Fehler...", str(e), "Fehler ")
                elif box.clickedButton() == buttonChange:
                    self.importSecurtiyData(row, col)
            else:
                self.importSecurtiyData(row, col)
                
    def showButtonClick(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = uiDatabaseWindow()
        self.ui.setupUi(self.window)
        self.window.setFixedSize(1226, 730)
        self.ui.cbSort.addItems(cabinnetsListExtend)
        self.creatingTables()
        self.ui.btnDelete.clicked.connect(self.deleteButtonClick)
        self.ui.btnEditSave.clicked.connect(self.editSaveClick)
        self.ui.btnSearch.clicked.connect(self.searchButtonClick)
        self.ui.tableWidget.cellClicked.connect(self.clickedDatasheetColumn)
        self.ui.tableWidget.cellChanged.connect(self.changedCommentSetColor)
        self.ui.cbSort.currentIndexChanged.connect(self.sortByCabinnets)
        self.window.show()

    def sortByCabinnets(self):
        selectedCabinnets = self.ui.cbSort.currentText()
        numberOfRows = self.ui.tableWidget.rowCount()
        if(selectedCabinnets == cabinnetsListExtend[0]):
            for rowIndex in range(0, numberOfRows):
                self.ui.tableWidget.setRowHidden(rowIndex, False)
        else:
            for rowIndex in range(0, numberOfRows):
                twItem = self.ui.tableWidget.item(rowIndex, cabinetsCol)
                if twItem.text() == selectedCabinnets:
                    self.ui.tableWidget.setRowHidden(rowIndex, False)
                else:
                    self.ui.tableWidget.setRowHidden(rowIndex, True)

    def searchButtonClick(self):
        searchInput = self.ui.teSearch.toPlainText()
        numberOfRows = self.ui.tableWidget.rowCount()
        if(searchInput != ""):
            for row in range(0, numberOfRows): 
                self.ui.tableWidget.setRowHidden(row, True) 

            items = self.ui.tableWidget.findItems(searchInput, QtCore.Qt.MatchContains)
            for item in items:
                self.ui.tableWidget.setRowHidden(item.row(), False)
        else:
            for row in range(0, numberOfRows): 
                self.ui.tableWidget.setRowHidden(row, False) 

    def deleteDatasheetInServer(self, fileName):
        try:
            ftp = FTP()  
            ftp.connect(self.databaseHost, portFTPServer)
            ftp.login(userFTPServer, passwordFTPServer)  

            ftp.delete(fileName)
            ftp.quit()
        except Exception as e:
            errorCode = ""
            if(str(e) in "[Errno 111] Connection refused"):
                errorCode = "FTP Server in Master ist noch nicht gestartet."
            else:
                errorCode = str(e)
            self.showMessage(QMessageBox.Critical, "Fehler wenn datenblatt gelöscht im Master", errorCode, "Fehler ")

    def delteDatasheet(self, records, datasheetName):
        if(len(records) == 1):
            if(datasheetName != ""):
                #Remove local datasheet:
                if os.path.exists(currentRunningFolder+securityDataSheetFolderPath+"/"+datasheetName+".pdf"):
                    os.remove(currentRunningFolder+securityDataSheetFolderPath+"/"+datasheetName+".pdf")
                #Remove from server if current is slave
                if(self.isCurrentComputerMasterSlave() is False): #Slave => Delete file in server
                    self.deleteDatasheetInServer(datasheetName+".pdf")

    def deleteButtonClick(self):
        selectedRow = self.ui.tableWidget.currentRow()
        if(selectedRow == -1):
            self.showMessage(QMessageBox.Critical, "Fehler", "Selektiert mindensten ein Zeil", "Fehler ")
        else:
            #Search No. number in database
            currentNo = self.ui.tableWidget.item(selectedRow, noCol).text()
            nameChemicals = self.ui.tableWidget.item(selectedRow, nameChemicalsCol).text()
            cabinets = self.ui.tableWidget.item(selectedRow, cabinetsCol).text()

            try:
                connection = mysql.connector.connect(host=self.databaseHost,
                                                        database=database,
                                                        user=databaseUser,
                                                        password=databasePassword)
                #Get datasheet name
                sql = "select securitydata from "+databaseTable+" where no='"+str(currentNo)+"'"
                cursor = connection.cursor()
                cursor.execute(sql)
                datasheetName = cursor.fetchone()[0]
                 
                #Get list of datasheet name to check any chemical uses same datasheet
                sql = "select securitydata from "+databaseTable+" where securitydata='"+datasheetName+"'"
                cursor = connection.cursor()
                cursor.execute(sql)
                records = cursor.fetchall()

                #Delete from table                                        
                sql = "delete from "+databaseTable+" where no='"+str(currentNo)+"'"
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()

                #Remove row in current table
                self.ui.tableWidget.removeRow(selectedRow)
                #Delete datasheet
                self.delteDatasheet(records, datasheetName)
                #Update last No
                self.displayLastNoInDatabase()

                self.showMessage(QMessageBox.Information, "Feritg!", "Erfolgreich gelöscht Objekt No."+currentNo+" mit Name von Chemikals "+nameChemicals+" im Schrank "+cabinets, "Infos")
            except mysql.connector.Error as err:
                self.showMessage(QMessageBox.Critical, "Fehler...", "Fehler "+str(err), "Fehler ")
            finally:
                if (connection.is_connected()):
                    cursor.close()
                    connection.close()

    def saveChanged(self, changeNoList, rows, cursor, connection):
        if(len(changeNoList) == 0):
            self.showMessage(QMessageBox.Information, "Infos", "Fertig!", "Information")
            self.window.close()
        else:
            for row in range(rows):
                changedNo = self.ui.tableWidget.item(row, noCol).text()
                if changedNo in changeNoList:
                    changedNameOfChemicals = self.ui.tableWidget.item(row, nameChemicalsCol).text()
                    changedCabinets = self.ui.tableWidget.item(row, cabinetsCol).text()
                    changedCasNumber = self.ui.tableWidget.item(row, casNumberCol).text()
                    changedSupplier = self.ui.tableWidget.item(row, supplierCol).text()
                    changedQuantity = self.ui.tableWidget.item(row, quantityCol).text()
                    if(not self.ui.tableWidget.item(row, quantityAmountCol).text().isnumeric()): #Check if quantity number is numeric
                        self.showMessage(QMessageBox.Critical, "Eingabe Fehler!", "Eingabe Stückzahl in Zeil "+str(row+1)+" ist nicht nummer!", "Fehler ")
                        return
                    changedQuantityNumber = self.ui.tableWidget.item(row, quantityAmountCol).text()
                    changedPerson = self.ui.tableWidget.item(row, personCol).text()
                    changedSecurityData = self.ui.tableWidget.item(row, securityDataCol).text()
                    if(not self.is_date(self.ui.tableWidget.item(row, dateCol).text())): #Check if new string input is date
                        self.showMessage(QMessageBox.Critical, "Eingabe Fehler!", "Eingabe Datum in Zeil "+str(row+1)+" ist nicht korrekt!", "Fehler ")
                        return
                    changedInputDate = datetime.strptime(self.ui.tableWidget.item(row, dateCol).text(), '%d-%m-%Y').date()
                    changedComment = self.ui.tableWidget.item(row, commentCol).text()
                    updateSql = "update "+databaseTable+" set name_of_chemicals ='"+changedNameOfChemicals+"', cabinets = '"+changedCabinets+"', cas_number = '"+str(changedCasNumber)+"', supplier = '"+str(changedSupplier)+"', quantity = '"+str(changedQuantity)+"', quantity_number = '"+str(changedQuantityNumber)+"', person = '"+changedPerson+"' , securitydata = '"+changedSecurityData+"' , input_date = '"+str(changedInputDate)+"', comment = '"+changedComment+"' where no="+str(changedNo)
                    cursor.execute(updateSql)
                    connection.commit()
            #Run successful windows here
            self.showMessage(QMessageBox.Information, "Erfolgreich", "Erfolgreich ändert in Datenbank", "Information")
            self.window.close()

    def saveAllNoOfAnyChange(self, no, row, rows, cabinets):
        #Check if string No. is number
        if(not no.isnumeric()):
            self.showMessage(QMessageBox.Critical, "Eingabe Fehler!", "Eingabe No. in Zeil "+str(row+1)+" ist nicht nummer!", "Fehler ")
            return
        elif(not cabinets in cabinnetsList):
            self.showMessage(QMessageBox.Critical, "Eingabe Fehler!", "Eingabe Schrank in Zeil "+str(row+1)+" ist nicht korrekt!", "Fehler ")
            return
        else:
            #Need to check if new No. already exist in table/database
            noExistList = self.isMoreNoExist(rows, no)
            if(len(noExistList) > 1): #More than 1 No. exist in table
                self.showMessage(QMessageBox.Critical, "Eingabe Fehler!", "Mehr No. "+str(no)+" existiert in Zeile: "+str(noExistList)+"!", "Fehler ")
                return
            else:
                return no

    def isItemChanged(self, row, records):
        changeBool = False
        for col in range(columns):
            dataFromTable = self.ui.tableWidget.item(row, col).text()
            dataFromDatabase = records[row-1][col+1]

            if col == columns-2: # This is "date" column => Need to format to compare
                dataFromDatabase = dataFromDatabase.strftime("%d-%m-%Y")
            if str(dataFromTable) != str(dataFromDatabase):
                changeBool = True
        return changeBool

    def editSaveClick(self):
        try:
            connection = mysql.connector.connect(host=self.databaseHost,
                                                    database=database,
                                                    user=databaseUser,
                                                    password=databasePassword)
            sql = "select * from "+databaseTable+" order by no"
            cursor = connection.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            rows = cursor.rowcount

            changeNoList = []
            #Compare data in table and database
            for row in range(rows):
                #Get No. of row, where table changed
                no = self.ui.tableWidget.item(row, noCol).text()
                cabinets = self.ui.tableWidget.item(row, cabinetsCol).text()
                
                #Check if item changed
                changeBool = self.isItemChanged(row, records)

                #If any change in table => save No of changed items    
                if changeBool:
                    changeNo = self.saveAllNoOfAnyChange(no, row, rows, cabinets) #Debug: check cabinets here!!!!!!!
                    changeNoList.append(changeNo)
            
            if(not None in changeNoList):
                #Save changed to database
                self.saveChanged(changeNoList, rows, cursor, connection)
        except mysql.connector.Error as err:
            self.showMessage(QMessageBox.Critical, "Fehler...", "Fehler "+str(err), "Fehler ")
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
            
    def onHeaderClicked(self, logicalIndex):
        self.ui.tableWidget.setSortingEnabled(True)
        if(logicalIndex == 0):
            pass #It sorts as string, not number
        else:
            currentSelectTimes = self.counterClickedHeader

            if(currentSelectTimes%2 == 0):
                self.ui.tableWidget.sortItems(logicalIndex, QtCore.Qt.AscendingOrder)
            else:
                self.ui.tableWidget.sortItems(logicalIndex, QtCore.Qt.DescendingOrder)

            currentSelectTimes += 1
            self.counterClickedHeader = currentSelectTimes

    def setBackgroundColor(self, tableRow, color):
        self.ui.tableWidget.item(tableRow, noCol).setBackground(color)
        self.ui.tableWidget.item(tableRow, nameChemicalsCol).setBackground(color)
        self.ui.tableWidget.item(tableRow, cabinetsCol).setBackground(color)
        self.ui.tableWidget.item(tableRow, casNumberCol).setBackground(color)
        self.ui.tableWidget.item(tableRow, supplierCol).setBackground(color)
        self.ui.tableWidget.item(tableRow, quantityCol).setBackground(color)
        self.ui.tableWidget.item(tableRow, quantityAmountCol).setBackground(color)
        self.ui.tableWidget.item(tableRow, personCol).setBackground(color)
        self.ui.tableWidget.item(tableRow, securityDataCol).setBackground(color)
        self.ui.tableWidget.item(tableRow, dateCol).setBackground(color)
        self.ui.tableWidget.item(tableRow, commentCol).setBackground(color)

    def setBackgroundColorForCommentRow(self, tableRow, comment):
        isNumberExistInComment = False

        for elem in redMarkingCommentList:
            if(comment.find(elem) != -1):
                isNumberExistInComment = True
        
        if(isNumberExistInComment):
            color = QtGui.QColor(255,0,0)
        else:
            color = QtGui.QColor(0,0,0,0)

        self.setBackgroundColor(tableRow, color)

    def setDatasheetRow(self, ro, datasheetPath, isForCreateRowFunc):
        if(datasheetPath != ""):
            datasheetPathSplit = datasheetPath.split("/", -1)
            fileName = datasheetPathSplit[-1]
            if(fileName.endswith(".pdf")):
                fileName = fileName[:-4]
            
            self.ui.tableWidget.setItem(ro, securityDataCol, QTableWidgetItem(str(fileName)))
            self.ui.tableWidget.item(ro, securityDataCol).setIcon(QtGui.QIcon(os.path.dirname(os.path.abspath(__file__))+"/icon/pdf.png"))

            #Set color for row
            if(isForCreateRowFunc is False):
                comment = self.ui.tableWidget.item(ro, commentCol).text()
                self.setBackgroundColorForCommentRow(ro, comment)
        else:
            self.ui.tableWidget.setItem(ro, securityDataCol, QTableWidgetItem(datasheetPath))
            
    def createRow(self):
        #Create rows
        try:
            connection = mysql.connector.connect(host=self.databaseHost,
                                                    database=database,
                                                    user=databaseUser,
                                                    password=databasePassword)
            sql = "select * from "+databaseTable+" order by no"
            cursor = connection.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            rows = cursor.rowcount
            
            self.ui.tableWidget.setRowCount(rows)

            ro = 0 #number ro in actual table/qtablewidget
            for row in records:
                self.ui.tableWidget.setItem(ro,noCol, QTableWidgetItem(str(row[noCol+1])))
                self.ui.tableWidget.setItem(ro,nameChemicalsCol, QTableWidgetItem(row[nameChemicalsCol+1]))
                self.ui.tableWidget.setItem(ro,cabinetsCol, QTableWidgetItem(row[cabinetsCol+1]))
                self.ui.tableWidget.setItem(ro,casNumberCol, QTableWidgetItem(row[casNumberCol+1]))
                self.ui.tableWidget.setItem(ro,supplierCol, QTableWidgetItem(row[supplierCol+1]))
                self.ui.tableWidget.setItem(ro,quantityCol, QTableWidgetItem(row[quantityCol+1]))
                self.ui.tableWidget.setItem(ro,quantityAmountCol, QTableWidgetItem(str(row[quantityAmountCol+1])))
                self.ui.tableWidget.setItem(ro,personCol, QTableWidgetItem(row[personCol+1]))
                
                datasheet = str(row[securityDataCol+1])
                self.setDatasheetRow(ro, datasheet, True)
                
                self.ui.tableWidget.setItem(ro,dateCol, QTableWidgetItem(row[dateCol+1].strftime("%d-%m-%Y")))
                self.ui.tableWidget.setItem(ro,commentCol, QTableWidgetItem(row[commentCol+1]))
                
                self.setBackgroundColorForCommentRow(ro, row[commentCol+1])
                ro+=1
        except mysql.connector.Error as err:
            self.showMessage(QMessageBox.Critical, "Fehler...", "Fehler "+str(err), "Fehler ")
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()

    def creatingTables(self):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(columns)
        
        self.ui.tableWidget.verticalHeader().setVisible(False) #Hide row number

        self.ui.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.ui.tableWidget.setSelectionMode(QTableWidget.SingleSelection)

        #Title of columns        
        self.ui.tableWidget.setHorizontalHeaderLabels(columnsList)
        self.ui.tableWidget.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)

        #Set width columns
        self.ui.tableWidget.setColumnWidth(noCol, noColWidth)
        self.ui.tableWidget.setColumnWidth(nameChemicalsCol, nameChemicalsColWidth)
        self.ui.tableWidget.setColumnWidth(cabinetsCol, cabinetsColWidth)
        self.ui.tableWidget.setColumnWidth(casNumberCol, casNumberColWidth)
        self.ui.tableWidget.setColumnWidth(supplierCol, supplierColWidth)
        self.ui.tableWidget.setColumnWidth(quantityCol, quantityColWidth)
        self.ui.tableWidget.setColumnWidth(quantityAmountCol, quantityAmountColWidth)
        self.ui.tableWidget.setColumnWidth(personCol, personColWidth)
        self.ui.tableWidget.setColumnWidth(securityDataCol, securityColWidth)
        self.ui.tableWidget.setColumnWidth(dateCol, dateColWidth)
        self.ui.tableWidget.setColumnWidth(commentCol, commentColWidth)
        
        delegate = ReadOnlyDelegate(self)
        self.ui.tableWidget.setItemDelegateForColumn(noCol, delegate) #Set readonly for No. column
        self.ui.tableWidget.setItemDelegateForColumn(securityDataCol, delegate) #Set readonly for Sicherheitsdatei. column

        self.createRow()


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        QtCore.QCoreApplication.setOrganizationName("Fraunhofer Umsicht")
        QtCore.QCoreApplication.setOrganizationDomain("www.umsicht.fraunhofer.de")
        QtCore.QCoreApplication.setApplicationName("Speicherte List von Chemikals des Batterielabors CL25")
        myWindow = MainWindow()
        myWindow.setFixedSize(myWindow.size())
        myWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Fehler...")
        if str(e) in "local variable 'connection' referenced before assignment":
            msg.setInformativeText("Fehler in der Verbindung mit Datenbank!")
        else:
            msg.setInformativeText(str(e))
        msg.setWindowTitle("Fehler")
        msg.exec_()
            

###
# 
#   Created by Anh Tu Nguyen. Email: anhtu91@gmail.com
#   Supervisor Rasit Özgüc. Email: rasit.oezguec@umsicht.fraunhofer.de
#   Bug is every where. Calm down and be patient. Everything has its own solution.
#
###
