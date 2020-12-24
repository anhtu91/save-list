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

import xlrd #For import from excel 
import xlwt #For export to excel
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
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem, QStyledItemDelegate
from PyQt5.QtCore import QUrl, QRegExp
from PyQt5.QtGui import QIcon, QRegExpValidator

from showdata import uiShowDataWindow

from dateutil.parser import parse
from datetime import datetime, date


#Change these lines for appropriate MySql server
databaseTable = "xxxxxxx"
database = "xxxxxxx"
databasePassword = "xxxxxxxx"
databaseUser = "xxxxxxx"
databaseLocalhost = "localhost"

#FTP Server config
userFTPServer = "xxxxxxxxxx"
passwordFTPServer = "xxxxxxxxx"
portFTPServer = 1026

#Save setting and datasheet folder
saveLastIPAddressFile = "setting"
securityDataSheetFolderPath = "/security_datasheet"
currentRunningFolder = str(os.path.dirname(os.path.abspath(__file__)))


strNo = "No."
strNameChemicalsCol = "Name of Chemical"
strNameCASNumberCol = "CAS-Number"
strSupplierCol = "Supplier"
strQuantityCol = "Quantity"
strQuantityAmountCol = "#"
strCommentCol = "H Sätze"


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


noColExcel = 0
nameChemicalsColExcel = 1
casNumberColExcel = 2
supplierColExcel = 3
quantityColExcel = 4
quantityAmountColExcel = 5
commentColExcel = 6


noColWidth = 50
nameChemicalsColWidth = 430
cabinetsColWidth = 200
casNumberColWidth = 150
supplierColWidth = 200
quantityColWidth = 100
quantityAmountColWidth = 100
personColWidth = 180
securityColWidth = 500
dateColWidth = 150
commentColWidth = 315

columnsList = ['No.', 'Chemikalienbezeichnung', 'Schrank', 'CAS-Nummer', 'Lieferant', 'g\ml', 'Stückzahl', 'Zuständig', 'Sicherheitsdatenblatt','Datum', 'H-Sätze']
columns = len(columnsList) #Number of columns in database table/ Change when add more columns

#Keep two following list sync ###cabinnetsList and ###cabinnetsListInExcel
cabinnetsList = [
    "CL25_Chem",
    "CL25_Gefahrstoff",
    "CL25_Gift",
    "CL22_Chem"
]

cabinnetsListInExcel = [
    "CL25_Chemikalienschrank",
    "CL25_Gefahrstoffschrank",
    "CL25_Giftschrank",
    "CL22_Chemikalienschrank"
]

#Change this list item to change marking red in table
redMarkingCommentList = ["300", "310", "330", "301", "311", "331", "340", "350", "360", "370", "372"]

cabinnetsListExtend = cabinnetsList.copy()
cabinnetsListExtend.insert(0,"Alle")

startDataRowExcelExportFile = 4
headerRowExcelExportFile = 0
headerColExcelExportFile = 2
headerListOfChemicals = "List of Chemicals"
headerSafetyCabinetBattLab = "Safety Cabinet BattLab"

markingColorNoticeRow = 15
markingColorNoticeCol = 9
markingColorNotice = "Rot Farbe: Giftstoff"
markingColorNoticeColWidth = 20

class Ui_ImportExport(object):
    def setupUi(self, ImportExport):
        ImportExport.setObjectName("ImportExport")
        ImportExport.resize(776, 457)
        self.centralwidget = QtWidgets.QWidget(ImportExport)
        self.centralwidget.setObjectName("centralwidget")
        self.btnImport = QtWidgets.QPushButton(self.centralwidget)
        self.btnImport.setGeometry(QtCore.QRect(20, 360, 351, 71))
        self.btnImport.setObjectName("btnImport")
        self.btnExport = QtWidgets.QPushButton(self.centralwidget)
        self.btnExport.setGeometry(QtCore.QRect(400, 360, 351, 71))
        self.btnExport.setObjectName("btnExport")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 130, 731, 212))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbPerson = QtWidgets.QLabel(self.layoutWidget)
        self.lbPerson.setObjectName("lbPerson")
        self.verticalLayout_2.addWidget(self.lbPerson)
        self.lbDatum = QtWidgets.QLabel(self.layoutWidget)
        self.lbDatum.setObjectName("lbDatum")
        self.verticalLayout_2.addWidget(self.lbDatum)
        self.lbdatasheet = QtWidgets.QLabel(self.layoutWidget)
        self.lbdatasheet.setObjectName("lbdatasheet")
        self.verticalLayout_2.addWidget(self.lbdatasheet)
        self.lbMasterSlaveOffline = QtWidgets.QLabel(self.layoutWidget)
        self.lbMasterSlaveOffline.setObjectName("lbMasterSlaveOffline")
        self.verticalLayout_2.addWidget(self.lbMasterSlaveOffline)
        self.lbIPAddress = QtWidgets.QLabel(self.layoutWidget)
        self.lbIPAddress.setObjectName("lbIPAddress")
        self.verticalLayout_2.addWidget(self.lbIPAddress)
        self.lbConnectionDatabase = QtWidgets.QLabel(self.layoutWidget)
        self.lbConnectionDatabase.setObjectName("lbConnectionDatabase")
        self.verticalLayout_2.addWidget(self.lbConnectionDatabase)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lePerson = QtWidgets.QLineEdit(self.layoutWidget)
        self.lePerson.setObjectName("lePerson")
        self.verticalLayout.addWidget(self.lePerson)
        self.dateEdit = QtWidgets.QDateEdit(self.layoutWidget)
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout.addWidget(self.dateEdit)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.leFolder = QtWidgets.QLineEdit(self.layoutWidget)
        self.leFolder.setObjectName("leFolder")
        self.horizontalLayout_5.addWidget(self.leFolder)
        self.btnBrowserFolder = QtWidgets.QPushButton(self.layoutWidget)
        self.btnBrowserFolder.setObjectName("btnBrowserFolder")
        self.horizontalLayout_5.addWidget(self.btnBrowserFolder)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.rbMaster = QtWidgets.QRadioButton(self.layoutWidget)
        self.rbMaster.setObjectName("rbMaster")
        self.horizontalLayout_3.addWidget(self.rbMaster)
        self.rbSlave = QtWidgets.QRadioButton(self.layoutWidget)
        self.rbSlave.setObjectName("rbSlave")
        self.horizontalLayout_3.addWidget(self.rbSlave)
        self.rbOffline = QtWidgets.QRadioButton(self.layoutWidget)
        self.rbOffline.setObjectName("rbOffline")
        self.horizontalLayout_3.addWidget(self.rbOffline)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.leIPAddress = QtWidgets.QLineEdit(self.layoutWidget)
        self.leIPAddress.setObjectName("leIPAddress")
        self.horizontalLayout_4.addWidget(self.leIPAddress)
        self.btnConnect = QtWidgets.QPushButton(self.layoutWidget)
        self.btnConnect.setObjectName("btnConnect")
        self.horizontalLayout_4.addWidget(self.btnConnect)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.lbConnection = QtWidgets.QLabel(self.layoutWidget)
        self.lbConnection.setText("")
        self.lbConnection.setPixmap(QtGui.QPixmap(os.path.dirname(os.path.abspath(__file__))+"/icon/not-ok.png"))
        self.lbConnection.setObjectName("lbConnection")
        self.verticalLayout.addWidget(self.lbConnection)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(20, 0, 731, 121))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbFraunhoferIcon = QtWidgets.QLabel(self.layoutWidget_2)
        self.lbFraunhoferIcon.setText("")
        self.lbFraunhoferIcon.setPixmap(QtGui.QPixmap(os.path.dirname(os.path.abspath(__file__))+"/icon/fraunhofer_small_icon.jpg"))
        self.lbFraunhoferIcon.setObjectName("lbFraunhoferIcon")
        self.horizontalLayout_2.addWidget(self.lbFraunhoferIcon)
        self.lbContact = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lbContact.setFont(font)
        self.lbContact.setObjectName("lbContact")
        self.horizontalLayout_2.addWidget(self.lbContact)
        ImportExport.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ImportExport)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 776, 26))
        self.menubar.setObjectName("menubar")
        ImportExport.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ImportExport)
        self.statusbar.setObjectName("statusbar")
        ImportExport.setStatusBar(self.statusbar)

        self.retranslateUi(ImportExport)
        QtCore.QMetaObject.connectSlotsByName(ImportExport)

    def retranslateUi(self, ImportExport):
        _translate = QtCore.QCoreApplication.translate
        ImportExport.setWindowTitle(_translate("ImportExport", "Importieren und Exportieren Datenbank "))
        self.btnImport.setText(_translate("ImportExport", "Importieren von Excel Datei (*.csv, *.xlsx)"))
        self.btnExport.setText(_translate("ImportExport", "Exportieren nach Excel Datei (*.csv, *.xlsx)"))
        self.lbPerson.setText(_translate("ImportExport", "Person"))
        self.lbDatum.setText(_translate("ImportExport", "Datum"))
        self.lbdatasheet.setText(_translate("ImportExport", "Sicherheitdateiordner"))
        self.lbMasterSlaveOffline.setText(_translate("ImportExport", "Betriebsart"))
        self.lbIPAddress.setText(_translate("ImportExport", "IP Adress von Master"))
        self.lbConnectionDatabase.setText(_translate("ImportExport", "Verbindung mit Datenbank"))
        self.dateEdit.setDisplayFormat(_translate("ImportExport", "dd-MM-yyyy"))
        self.btnBrowserFolder.setText(_translate("ImportExport", "Browser"))
        self.rbMaster.setText(_translate("ImportExport", "Master"))
        self.rbSlave.setText(_translate("ImportExport", "Slave"))
        self.rbOffline.setText(_translate("ImportExport", "Offline"))
        self.btnConnect.setText(_translate("ImportExport", "Verbinden"))
        self.lbContact.setText(_translate("ImportExport", "Raumkoordinator: Rasit Özgüc\n"
"Durchwahl: -1141\n"
"E-Mail: rasit.oezguec@umsicht.fraunhofer.de"))
        

class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return

class MyWindow(QtWidgets.QMainWindow, Ui_ImportExport):
    counterClickedHeader = 0
    dictRowChemicalsName = {}
    databaseHost = "" 

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_ImportExport.__init__(self)
        self.setupUi(self)
        today = date.today()
        self.dateEdit.setDate(today)
        self.leFolder.setDisabled(True)

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
        self.btnImport.clicked.connect(self.btnImportClicked)
        self.btnExport.clicked.connect(self.btnExportClicked)
        self.btnBrowserFolder.clicked.connect(self.btnBrowserClicked)

    def clickedRadioBoxMaster(self):
        self.leIPAddress.setEnabled(False)
        self.btnConnect.setEnabled(False)
        #if self.window.show:
        #    self.window.close()
        self.databaseHost = self.getCurrentIP()
        self.testConnectionWithDatabase()

    def clickedRadioBoxSlave(self):
        self.leIPAddress.setEnabled(True)
        self.btnConnect.setEnabled(True)
        self.lbConnection.setPixmap(QtGui.QPixmap(os.path.dirname(os.path.abspath(__file__))+"/icon/not-ok.png"))

    def clickedRadioBoxOffline(self):
        self.leIPAddress.setEnabled(False)
        self.btnConnect.setEnabled(False)
        #if self.window.show:
        #    self.window.close()
        self.databaseHost = databaseLocalhost
        self.testConnectionWithDatabase()

    def updateIPAddressServer(self):
        self.databaseHost = self.leIPAddress.text()

        saveLastIPFilePath = currentRunningFolder+"/"+saveLastIPAddressFile
        if(os.path.isfile(saveLastIPFilePath) is True):
            lastIpFile = open(saveLastIPFilePath, "w+")
            lastIP = lastIpFile.read()
            if(lastIP != self.databaseHost):
                lastIpFile.write(self.databaseHost)

        self.testConnectionWithDatabase()

    def testConnectionWithDatabase(self):
        isConnecting = False
        try:
            connection = mysql.connector.connect(host=self.databaseHost,
                                                    database=database,
                                                    user=databaseUser,
                                                    password=databasePassword)
            sql = "select * from "+databaseTable
            cursor = connection.cursor()
            cursor.execute(sql)
            
            self.lbConnection.setPixmap(QtGui.QPixmap(os.path.dirname(os.path.abspath(__file__))+"/icon/ok.png"))
            isConnecting = True
        except mysql.connector.Error as err:
            msg = QMessageBox()
            self.showMessage(msg, QMessageBox.Critical, "Fehler...", "Fehler "+str(err), "Fehler ")
            self.lbConnection.setPixmap(QtGui.QPixmap(os.path.dirname(os.path.abspath(__file__))+"/icon/not-ok.png"))
            isConnecting = False
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
            return isConnecting

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

    def is_date(self, string, fuzzy=False):
        try: 
            parse(string, fuzzy=fuzzy)
            return True
        except ValueError:
            return False

    def btnBrowserClicked(self):
        msg = QMessageBox()
        try:
            folderName = QFileDialog.getExistingDirectory(self, 'Ordner auswählen', options=QFileDialog.DontUseNativeDialog)
            if(folderName != currentRunningFolder+securityDataSheetFolderPath):
                self.leFolder.setText(folderName)
            else:
                self.showMessage(msg, QMessageBox.Critical, "Fehler...","Darf nicht gespeicherte Datenblätter selektieren", "Fehler ")
        except Exception as e:
            self.showMessage(msg, QMessageBox.Critical, "Fehler...", str(e), "Fehler ")

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

    def insertHeaderExcel(self, sheet):
        firstHeaderStyle = xlwt.XFStyle()
        secondHeaderStyle = xlwt.XFStyle()
        style = xlwt.XFStyle()

        #font header
        firstHeaderFont = xlwt.Font()
        firstHeaderFont.height = 320 # 16 * 20, for 16 point
        firstHeaderFont.bold = True
        firstHeaderStyle.font = firstHeaderFont

        secondHeaderFont = xlwt.Font()
        secondHeaderFont.height = 320 # 16 * 20, for 16 point
        secondHeaderStyle.font = secondHeaderFont

        sheet.write(headerRowExcelExportFile, headerColExcelExportFile, headerListOfChemicals, firstHeaderStyle)
        sheet.row(headerRowExcelExportFile).height_mismatch = True
        sheet.row(headerRowExcelExportFile).height = 350
        sheet.write(headerRowExcelExportFile+1, headerColExcelExportFile, headerSafetyCabinetBattLab+" "+sheet.name, secondHeaderStyle)
        sheet.row(headerRowExcelExportFile+1).height_mismatch = True
        sheet.row(headerRowExcelExportFile+1).height = 350
        sheet.write(headerRowExcelExportFile+2, headerColExcelExportFile+2, "Update: "+self.dateEdit.text(), secondHeaderStyle)
        sheet.row(headerRowExcelExportFile+2).height_mismatch = True
        sheet.row(headerRowExcelExportFile+2).height = 350

        styleMarkingColor = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour')
        sheet.write(markingColorNoticeRow, markingColorNoticeCol, markingColorNotice, styleMarkingColor)
        sheet.col(markingColorNoticeCol).width = (markingColorNoticeColWidth*367)

        # font
        font = xlwt.Font()
        font.bold = True
        style.font = font

        sheet.write(startDataRowExcelExportFile, noColExcel+1, strNo, style)
        sheet.write(startDataRowExcelExportFile, nameChemicalsColExcel+1, strNameChemicalsCol, style)
        sheet.write(startDataRowExcelExportFile, casNumberColExcel+1, strNameCASNumberCol, style)
        sheet.write(startDataRowExcelExportFile, supplierColExcel+1, strSupplierCol, style)
        sheet.write(startDataRowExcelExportFile, quantityColExcel+1, strQuantityCol, style)
        sheet.write(startDataRowExcelExportFile, quantityAmountColExcel+1, strQuantityAmountCol, style)
        sheet.write(startDataRowExcelExportFile, commentColExcel+1, strCommentCol, style)


    def maxHeaderColWidth(self):
        maxColWidth = []
        maxColWidth.insert(noColExcel, len(strNo))
        maxColWidth.insert(nameChemicalsColExcel, len(headerSafetyCabinetBattLab+" "+cabinnetsList[0]))
        maxColWidth.insert(casNumberColExcel, len(strNameCASNumberCol))
        maxColWidth.insert(supplierColExcel, len(strSupplierCol))
        maxColWidth.insert(quantityColExcel, len(strQuantityCol))
        maxColWidth.insert(quantityAmountColExcel, len(strQuantityAmountCol))
        maxColWidth.insert(commentColExcel, len(strCommentCol))
        return maxColWidth

    def insertDataToExcel(self, sheet, records, row, noSheet, maxColWidth):
        dataNoSheet = str(noSheet-startDataRowExcelExportFile)
        dataNameChemicals = str(records[row][nameChemicalsCol+1]).strip()
        dataCasNumber = str(records[row][casNumberCol+1]).strip()
        dataSupplier = str(records[row][supplierCol+1]).strip()
        dataQuantity = str(records[row][quantityCol+1]).strip()
        dataQuantityAmount = str(records[row][quantityAmountCol+1]).strip()
        dataComment = str(records[row][commentCol+1]).strip()

        if maxColWidth[noColExcel] < len(dataNoSheet): maxColWidth.insert(noColExcel, len(dataNoSheet))
        if maxColWidth[nameChemicalsColExcel] < len(dataNameChemicals): maxColWidth.insert(nameChemicalsColExcel, len(dataNameChemicals))
        if maxColWidth[casNumberColExcel] < len(dataCasNumber): maxColWidth.insert(casNumberColExcel, len(dataCasNumber))
        if maxColWidth[supplierColExcel] < len(dataSupplier): maxColWidth.insert(supplierColExcel, len(dataSupplier))
        if maxColWidth[quantityColExcel] < len(dataQuantity): maxColWidth.insert(quantityColExcel, len(dataQuantity))
        if maxColWidth[quantityAmountColExcel] < len(dataQuantityAmount): maxColWidth.insert(quantityAmountColExcel, len(dataQuantityAmount))
        if maxColWidth[commentColExcel] < len(dataComment): maxColWidth.insert(commentColExcel, len(dataComment))

        style = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour')
        if(self.checkCommentForSetColor(dataComment)):
            sheet.write(noSheet, noColExcel+1, dataNoSheet, style)
            sheet.write(noSheet, nameChemicalsColExcel+1, dataNameChemicals, style)
            sheet.write(noSheet, casNumberColExcel+1, dataCasNumber, style)
            sheet.write(noSheet, supplierColExcel+1, dataSupplier, style)
            sheet.write(noSheet, quantityColExcel+1, dataQuantity, style)
            sheet.write(noSheet, quantityAmountColExcel+1, dataQuantityAmount, style)
            sheet.write(noSheet, commentColExcel+1, dataComment, style)
        else:
            sheet.write(noSheet, noColExcel+1, dataNoSheet)
            sheet.write(noSheet, nameChemicalsColExcel+1, dataNameChemicals)
            sheet.write(noSheet, casNumberColExcel+1, dataCasNumber)
            sheet.write(noSheet, supplierColExcel+1, dataSupplier)
            sheet.write(noSheet, quantityColExcel+1, dataQuantity)
            sheet.write(noSheet, quantityAmountColExcel+1, dataQuantityAmount)
            sheet.write(noSheet, commentColExcel+1, dataComment)

        return maxColWidth

    def setSheetColumnWidth(self, sheet, maxColWidth):
        sheet.col(noColExcel+1).width = (maxColWidth[noColExcel]*367)
        sheet.col(nameChemicalsColExcel+1).width = (maxColWidth[nameChemicalsColExcel]*367)
        sheet.col(casNumberColExcel+1).width = (maxColWidth[casNumberColExcel]*367)
        sheet.col(supplierColExcel+1).width = (maxColWidth[supplierColExcel]*400)
        sheet.col(quantityColExcel+1).width = (maxColWidth[quantityColExcel]*367)
        sheet.col(quantityAmountColExcel+1).width = (maxColWidth[quantityAmountColExcel]*367)
        sheet.col(commentColExcel+1).width = (maxColWidth[commentColExcel]*367)

    def insertDataToRowExcel(self, rows, records, cl25ChemikaSheet, cl25GefahrSheet, cl25GiftSheet, cl22ChemikaSheet, maxColWidthCl25Chemika, maxColWidthCl25Gefahr, maxColWidthCl25Gift, maxColWidthCl22Chemika):
        noCl25ChemikaSheet = startDataRowExcelExportFile+1
        noCl25GefahrSheet = startDataRowExcelExportFile+1
        noCl25GiftSheet = startDataRowExcelExportFile+1
        noCl22Chemika = startDataRowExcelExportFile+1

        for row in range(rows):
            cabinetName = records[row][cabinetsCol+1]
            if(cabinetName == cabinnetsList[0]): #Insert CL25_Chemika sheet
                maxColWidthCl25Chemika = self.insertDataToExcel(cl25ChemikaSheet, records, row, noCl25ChemikaSheet, maxColWidthCl25Chemika)
                noCl25ChemikaSheet += 1
            elif(cabinetName == cabinnetsList[1]): #Insert CL25_Elektrolyt sheet
                maxColWidthCl25Gefahr = self.insertDataToExcel(cl25GefahrSheet, records, row, noCl25GefahrSheet, maxColWidthCl25Gefahr)
                noCl25GefahrSheet += 1
            elif(cabinetName == cabinnetsList[2]): #Insert CL25_Gift sheet
                maxColWidthCl25Gift = self.insertDataToExcel(cl25GiftSheet, records, row, noCl25GiftSheet, maxColWidthCl25Gift)
                noCl25GiftSheet += 1
            elif(cabinetName == cabinnetsList[3]): #Insert CL22_Chemika sheet
                maxColWidthCl22Chemika = self.insertDataToExcel(cl22ChemikaSheet, records, row, noCl22Chemika, maxColWidthCl22Chemika)
                noCl22Chemika += 1
        return (maxColWidthCl25Chemika, maxColWidthCl25Gefahr, maxColWidthCl25Gift, maxColWidthCl22Chemika)

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
        except Exception:
            return False

    def exportDatasheet(self, rows, records):
        exportFolder = QFileDialog.getExistingDirectory(self,caption='Speichern Sicherheitsdatenblätter', options=QFileDialog.DontUseNativeDialog)
        downloadSuccessfulAllFile = True
        listFileFailedDownload = []
        counterDatasheetInDatabase = 0

        for row in range(rows):
            datasheet = records[row][securityDataCol+1]
            if(datasheet != ""):
                counterDatasheetInDatabase += 1
                if(os.path.isfile(currentRunningFolder+securityDataSheetFolderPath+"/"+datasheet+".pdf")): #If file exist in local => copy
                    try:
                        #Copy file to local save folder
                        shutil.copy2(currentRunningFolder+securityDataSheetFolderPath+"/"+datasheet+".pdf", exportFolder)
                    except Exception:
                        downloadSuccessfulAllFile = False
                        listFileFailedDownload.append(datasheet+".pdf")
                else: #If file not exist in local => Check Master/Slave/Offline
                    if(self.isCurrentComputerMasterSlave() is False): #Slave mode => try to download from server
                        downloadSuccessfulOneFile = self.downloadDatasheetFromMaster(datasheet+".pdf", exportFolder+"/"+datasheet+".pdf")
                        if(downloadSuccessfulOneFile is False):
                            downloadSuccessfulAllFile = False
                            listFileFailedDownload.append(datasheet+".pdf")

        msg = QMessageBox()
        if(downloadSuccessfulAllFile is True):
            self.showMessage(msg, QMessageBox.Information, "Info...", "Erfolgreich exportiert die Sicherheitsdatenblätter in den Ordner "+str(exportFolder), "Info")
        else:
            if(counterDatasheetInDatabase == len(listFileFailedDownload)):
                self.showMessage(msg, QMessageBox.Warning, "Sicherheitsdatei nicht exportiert", "Alle Sicherheitsdatenblätter wurde nicht exportiert! Versucht selbst copiert von dem Ordner "+currentRunningFolder+securityDataSheetFolderPath+" in Master.", "Warnung")
            else:
                self.showMessage(msg, QMessageBox.Warning, "Sicherheitsdatei nicht komplett exportiert", str(len(listFileFailedDownload))+" Sicherheitsdatenblätter wurde nicht exportiert: "+str(listFileFailedDownload)+". Versucht selbst copiert von dem Ordner "+currentRunningFolder+securityDataSheetFolderPath+" in Master.", "Warnung")

    def btnExportClicked(self):
        msg = QMessageBox()
        if(self.testConnectionWithDatabase() is True):
            try:
                filename = QFileDialog.getSaveFileName(self,caption='Speichern alle Infos in Excel Datei', filter="Excel Datei (*.xlsx)", options=QFileDialog.DontUseNativeDialog)
                wb = xlwt.Workbook()
                cl25ChemikaSheet = wb.add_sheet(cabinnetsListInExcel[0])
                cl25GefahrSheet = wb.add_sheet(cabinnetsListInExcel[1])
                cl25GiftSheet = wb.add_sheet(cabinnetsListInExcel[2])
                cl22ChemikaSheet = wb.add_sheet(cabinnetsListInExcel[3])

                xlwt.add_palette_colour("custom_colour", 0x21)
                wb.set_colour_RGB(0x21, 250, 0, 0)

                #Read data from database
                connection = mysql.connector.connect(host=self.databaseHost,
                                                        database=database,
                                                        user=databaseUser,
                                                        password=databasePassword)
                if connection.is_connected():
                    sql = "select * from "+databaseTable+" order by no desc"
                    cursor = connection.cursor()
                    cursor.execute(sql)
                    records = cursor.fetchall()
                    rows = cursor.rowcount

                    #Sort data by No.
                    records.sort(key=lambda tup: tup[1]) 

                    #Insert header
                    self.insertHeaderExcel(cl25ChemikaSheet)
                    self.insertHeaderExcel(cl25GefahrSheet)
                    self.insertHeaderExcel(cl25GiftSheet)
                    self.insertHeaderExcel(cl22ChemikaSheet)

                    #Max Column Width
                    maxColWidth = self.maxHeaderColWidth()
                    maxColWidthCl25Chemika = maxColWidth.copy()
                    maxColWidthCl25Gefahr = maxColWidth.copy()
                    maxColWidthCl25Gift = maxColWidth.copy()
                    maxColWidthCl22Chemika = maxColWidth.copy()                

                    #Insert data to row in excel
                    maxColWidth = self.insertDataToRowExcel(rows, records, cl25ChemikaSheet, cl25GefahrSheet, cl25GiftSheet, cl22ChemikaSheet, maxColWidthCl25Chemika, maxColWidthCl25Gefahr, maxColWidthCl25Gift, maxColWidthCl22Chemika)
                    maxColWidthCl25Chemika = maxColWidth[0]
                    maxColWidthCl25Gefahr = maxColWidth[1]
                    maxColWidthCl25Gift = maxColWidth[2]
                    maxColWidthCl22Chemika = maxColWidth[3]

                    #Set column width
                    self.setSheetColumnWidth(cl25ChemikaSheet, maxColWidthCl25Chemika)
                    self.setSheetColumnWidth(cl25GefahrSheet, maxColWidthCl25Gefahr)
                    self.setSheetColumnWidth(cl25GiftSheet, maxColWidthCl25Gift)
                    self.setSheetColumnWidth(cl22ChemikaSheet, maxColWidthCl22Chemika)
                    
                    if(filename[0] != ""):
                        #Save file
                        wb.save(filename[0]+".xlsx")
                        self.showMessage(msg, QMessageBox.Information, "Info...", "Erfolgreich in die Excel Datei exportieren", "Info")
                        self.exportDatasheet(rows, records)

            except Exception as err:
                self.showMessage(msg, QMessageBox.Critical, "Fehler...", "Fehler "+str(err), "Fehler ")
            finally:
                if (connection.is_connected()):
                    cursor.close()
                    connection.close()
        else:
            msg = QMessageBox()
            self.showMessage(msg, QMessageBox.Critical, "Fehler...", "Keine Verbindung mit Datenbank. Betriebsart muss selektiert werden!", "Fehler ")

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
    
    def setDatasheetRow(self, ro, datasheetPath):
        if(datasheetPath != ""):
            datasheetPathSplit = datasheetPath.split("/", -1)
            fileName = datasheetPathSplit[-1]
            if(fileName.endswith(".pdf")):
                fileName = fileName[:-4]
            
            self.ui.tableWidget.setItem(ro, securityDataCol, QTableWidgetItem(str(fileName)))
            self.ui.tableWidget.item(ro, securityDataCol).setIcon(QtGui.QIcon(os.path.dirname(os.path.abspath(__file__))+"/icon/pdf.png"))

            #Set color for row
            comment = self.ui.tableWidget.item(ro, commentCol).text()
            self.setBackgroundColorForCommentRow(ro, comment)
        else:
            self.ui.tableWidget.setItem(ro, securityDataCol, QTableWidgetItem(datasheetPath))

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
                        
                    self.setDatasheetRow(row, securityDataPath)
            except Exception as e:
                msg = QMessageBox()
                self.showMessage(msg, QMessageBox.Critical, "Fehler...", str(e), "Fehler ")

    def clickedDatasheetColumn(self, row, col):
        if(col == securityDataCol):
            securityDataSheet = self.ui.tableWidget.item(row, col).text()

            if(securityDataSheet != ""):
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
                    securityFilePath = currentRunningFolder+securityDataSheetFolderPath+"/"+securityDataSheet+".pdf"
                    if(securityFilePath != ""):
                        msg = QMessageBox()
                        #Check if security datasheet already exists in local save folder
                        if(os.path.isfile(securityFilePath) is False):    
                            self.showMessage(msg, QMessageBox.Critical, "Fehler...", "Gespeicherte Sicherheitsdatei unter dem Ordner wurde gelöscht!", "Fehler ")
                            return
                        #Use webbrowser to open pdf data
                        try:
                            webbrowser.open(securityFilePath)
                        except Exception as e:
                            self.showMessage(msg, QMessageBox.Critical, "Fehler...", str(e), "Fehler ")
                elif box.clickedButton() == buttonChange:
                    self.importSecurtiyData(row, col)
            else:
                self.importSecurtiyData(row, col)

    def btnImportClicked(self):
        if(self.testConnectionWithDatabase() is True):
            self.window = QtWidgets.QMainWindow()
            self.ui = uiShowDataWindow()
            self.ui.setupUi(self.window)
            self.window.setFixedSize(1226, 730)
            self.ui.cbSort.addItems(cabinnetsListExtend)
            self.dictRowChemicalsName.clear()
            self.creatingTables()
            self.ui.btnEditSave.clicked.connect(self.insertDataToDatabase)
            self.ui.btnSearch.clicked.connect(self.searchButtonClick)
            self.ui.tableWidget.cellClicked.connect(self.clickedDatasheetColumn)
            self.ui.tableWidget.cellChanged.connect(self.changedCommentSetColor)
            self.ui.cbSort.currentIndexChanged.connect(self.sortByCabinnets)
        else:
            msg = QMessageBox()
            self.showMessage(msg, QMessageBox.Critical, "Fehler...", "Keine Verbindung mit Datenbank. Betriebsart muss selektiert werden!", "Fehler ")

    def changedCommentSetColor(self, row, col):
        if(col == commentCol):
            newComment = self.ui.tableWidget.item(row, col).text()
            self.setBackgroundColorForCommentRow(row, newComment)

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

    def showMessage(self, msg, icon, strText, strInfoText, strTitle):
        msg.setIcon(icon)
        msg.setText(strText)
        msg.setInformativeText(strInfoText)
        msg.setWindowTitle(strTitle)
        msg.exec_()

    def creatingTables(self):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(columns)
        
        #Hide row number
        self.ui.tableWidget.verticalHeader().setVisible(False) 

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

        #Set readonly for No. column
        delegate = ReadOnlyDelegate(self)
        self.ui.tableWidget.setItemDelegateForColumn(noCol, delegate) 

        self.getDataFromExcel()

        if(self.leFolder.text() != ""):
            self.getSecurityDatasheet()

    def isCurrentComputerMasterSlave(self): #return True if master/offline mode activate, False if slave mode activates
        isMasterSlaveOffline = False
        if(self.rbMaster.isChecked() is True):
            isMasterSlaveOffline = True
        elif(self.rbOffline.isChecked() is True):
            isMasterSlaveOffline = True
        elif(self.rbSlave.isChecked() is True):
            isMasterSlaveOffline = False
        return isMasterSlaveOffline

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
            msg = QMessageBox()
            errorCode = ""
            if(str(e) in "[Errno 111] Connection refused"):
                errorCode = "FTP Server in Master ist noch nicht gestartet."
            else:
                errorCode = str(e)
            self.showMessage(msg, QMessageBox.Critical, "Fehler wenn datenblatt hochgeladen auf den Master", errorCode, "Fehler ")

    def getSecurityDatasheet(self):
        folderName = self.leFolder.text()
        directory = os.fsencode(folderName)
        counterChemicalsFoundDatasheet = 0
        listFileUsed = []
        listFileNotUsed = []
        listAllPdfFile = []

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".pdf"):
                listAllPdfFile.append(file)
                saveUsedFileToList = False
                for row in self.dictRowChemicalsName:
                    if(filename[:-4].lower() in self.dictRowChemicalsName[row].lower()):
                        #Copy file to local save folder
                        shutil.copy2(folderName+"/"+filename, currentRunningFolder+securityDataSheetFolderPath)
                        
                        #Check Master/Slave/Offline
                        if(self.isCurrentComputerMasterSlave() is False): #Slave => Upload datasheet to server
                            self.uploadDatasheetToServer(filename, currentRunningFolder+securityDataSheetFolderPath+"/"+filename)
                        
                        #Save local folder
                        securityData = filename[:-4]
                        
                        self.ui.tableWidget.setItem(row, securityDataCol, QTableWidgetItem(securityData))
                        self.ui.tableWidget.item(row, securityDataCol).setIcon(QtGui.QIcon(os.path.dirname(os.path.abspath(__file__))+"/icon/pdf.png"))
                        
                        comment = self.ui.tableWidget.item(row, securityDataCol).text()
                        self.setBackgroundColorForCommentRow(row, comment)
                        
                        counterChemicalsFoundDatasheet += 1
                        if(saveUsedFileToList == False):
                            listFileUsed.append(file)
                            saveUsedFileToList = True

        listFileNotUsed = list(set(listAllPdfFile) - set(listFileUsed))
        msg = QMessageBox()
        self.showMessage(msg, QMessageBox.Information, "Sicherheitsdatenblatt gefunden", "Gefunden "+str(len(listFileUsed))+" datenblatt für "+str(counterChemicalsFoundDatasheet)+" Chemikals. "+str(len(listFileNotUsed))+" datenblatt wurden nicht verwendet.", "Infos")

    def getDataFromExcel(self):
        try:
            filename = QFileDialog.getOpenFileName(self, "Datei auswählen",filter="Datei (*.xls *.xlsx)", options=QFileDialog.DontUseNativeDialog)
            path = filename[0]
            if(path != ""):
                # Give the location of the file 
                loc = (path) 
                
                # To open Workbook 
                wb = xlrd.open_workbook(loc) 
                # List Name of sheet
                listSheet = wb.sheet_names()
                
                #Total rows
                totalRows = self.countRowInExcel(wb, listSheet)
                #print(totalRows)
                
                self.ui.tableWidget.setRowCount(totalRows)
                tableRow = 0

                for i in range(len(listSheet)):

                    if(listSheet[i] == cabinnetsListInExcel[0]): #CL25_Chemikalienschrank
                        tableRow = self.getDataFromSheetInsertToTable(cabinnetsList[0], tableRow, cabinnetsListInExcel[0], i, wb)
                        
                    elif(listSheet[i] == cabinnetsListInExcel[1]): #CL25_Gefahrstoffschrank
                        tableRow = self.getDataFromSheetInsertToTable(cabinnetsList[1], tableRow, cabinnetsListInExcel[1], i, wb)

                    elif(listSheet[i]== cabinnetsListInExcel[2]): #CL25_Giftschrank
                        tableRow = self.getDataFromSheetInsertToTable(cabinnetsList[2], tableRow, cabinnetsListInExcel[2], i, wb)    

                    elif(listSheet[i]== cabinnetsListInExcel[3]): #CL22_Chemikalienschrank
                        tableRow = self.getDataFromSheetInsertToTable(cabinnetsList[3], tableRow, cabinnetsListInExcel[3], i, wb)     

                self.window.show()     
        except Exception as err:
            msg = QMessageBox()
            self.showMessage(msg, QMessageBox.Critical, "Fehler...", "Fehler "+str(err), "Fehler ")

    def getDataFromSheetInsertToTable(self, cabinnet, tableRow, sheetName, i, wb):
        sheet = wb.sheet_by_index(i)
        startRowStartCol = self.findStartRowStartCol(sheet)
        startRow = startRowStartCol[0]
        startCol = startRowStartCol[1]
        isTableFormCorrect = startRowStartCol[2]

        if(isTableFormCorrect):
            tableRow = self.insertDataToTable(sheet, startRow, startCol, tableRow, cabinnet)   
        else:
            msg = QMessageBox()
            self.showMessage(msg, QMessageBox.Critical, "Fehler...", "Die Form von Tabelle "+sheetName+" ist nicht korrekt", "Fehler ")
        
        return tableRow

    def countRowInExcel(self, wb, listSheet):
        totalRowNumber = 0
        
        for i in range(len(listSheet)):
            if(listSheet[i] == cabinnetsListInExcel[0]): #"CL25_Chemikalienschrank",
                cl25ChemikaSheet = wb.sheet_by_index(i)
                startCl25ChemikaRow = self.findStartRowStartCol(cl25ChemikaSheet)[0]
                totalRowNumber += cl25ChemikaSheet.nrows - startCl25ChemikaRow
            
            elif(listSheet[i] == cabinnetsListInExcel[1]): #"CL25_Gefahrstoffschrank",
                cl25GefahrSheet = wb.sheet_by_index(i)
                startCl25GefahrRow = self.findStartRowStartCol(cl25GefahrSheet)[0]
                totalRowNumber += cl25GefahrSheet.nrows - startCl25GefahrRow

            elif(listSheet[i] == cabinnetsListInExcel[2]): #"CL25_Giftschrank",
                cl25GiftSheet = wb.sheet_by_index(i)
                startCl25GiftRow = self.findStartRowStartCol(cl25GiftSheet)[0]
                totalRowNumber += cl25GiftSheet.nrows - startCl25GiftRow

            elif(listSheet[i] == cabinnetsListInExcel[3]): #"CL22_Chemikalienschrank"
                cl22ChemikaSheet = wb.sheet_by_index(i)
                startCl22ChemikaRow = self.findStartRowStartCol(cl22ChemikaSheet)[0]
                totalRowNumber += cl22ChemikaSheet.nrows - startCl22ChemikaRow

        return totalRowNumber

    def getLastNoFromDatabase(self):
        try:
            connection = mysql.connector.connect(host=self.databaseHost,
                                                    database=database,
                                                    user=databaseUser,
                                                    password=databasePassword)
            if connection.is_connected():
                sql = "select no from "+databaseTable+" order by no desc limit 1"
                cursor = connection.cursor()
                cursor.execute(sql)
                records = cursor.fetchone()
        except mysql.connector.Error as err:
            self.showMessage(msg, QMessageBox.Critical, "Fehler...", "Fehler "+str(err), "Fehler ")
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
            if(records is None): #For overwrite database
                return 0
            return records[0]

    def insertNewToDatabase(self, numberRowsTable, lastNoInDatabase=0):
        msg = QMessageBox()

        try:
            connection = mysql.connector.connect(host=self.databaseHost,
                                                    database=database,
                                                    user=databaseUser,
                                                    password=databasePassword)
            if connection.is_connected():
                sql = "insert into "+databaseTable+" (no, name_of_chemicals, cabinets, cas_number, supplier, quantity, quantity_number, person, securitydata, input_date, comment) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor = connection.cursor(buffered=True)

                for row in range(numberRowsTable):
                    nameChemical = self.ui.tableWidget.item(row, nameChemicalsCol).text()
                    schrank = self.ui.tableWidget.item(row, cabinetsCol).text()
                    casNumber = self.ui.tableWidget.item(row, casNumberCol).text()
                    supplier = self.ui.tableWidget.item(row, supplierCol).text()
                    quantity = self.ui.tableWidget.item(row, quantityCol).text()
                    if(not self.ui.tableWidget.item(row, quantityAmountCol).text().isnumeric()): #Check if quantity number is numeric
                        self.showMessage(msg, QMessageBox.Critical, "Eingabe Fehler!", "Eingabe Stückzahl in No. "+str(row+1)+" ist nicht nummer!", "Fehler ")
                        return
                    quantityAmount = self.ui.tableWidget.item(row, quantityAmountCol).text()
                    person = self.ui.tableWidget.item(row, personCol).text()
                    securityData = self.ui.tableWidget.item(row, securityDataCol).text()
                    if(not self.is_date(self.ui.tableWidget.item(row, dateCol).text())): #Check if new string input is date
                        self.showMessage(msg, QMessageBox.Critical, "Eingabe Fehler!", "Eingabe Datum in No. "+str(row+1)+" ist nicht korrekt!", "Fehler ")
                        return
                    date = str(datetime.strptime(self.ui.tableWidget.item(row, dateCol).text(), '%d-%m-%Y'))
                    comment = self.ui.tableWidget.item(row, commentCol).text()
                    lastNoInDatabase += 1

                    val = (lastNoInDatabase, nameChemical, schrank, casNumber, supplier, quantity, quantityAmount, person, securityData, date, comment)
                    cursor.execute(sql, val)
                    
                connection.commit()
                self.showMessage(msg, QMessageBox.Information, "Erfolgreich...", "Erfolgreich neue Datei eingefügt", "Info")
        except mysql.connector.Error as err:
            self.showMessage(msg, QMessageBox.Critical, "Fehler...", "Fehler "+str(err), "Fehler ")
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()  
              
    def overwriteNewDatabase(self, numberRowsTable):
        msg = QMessageBox()
        try:
            connection = mysql.connector.connect(host=self.databaseHost,
                                                    database=database,
                                                    user=databaseUser,
                                                    password=databasePassword)
            if connection.is_connected():
                #Check if table exists
                sqlTableExist = 'select * from information_schema.tables where table_schema="'+database+'" and table_name="'+databaseTable+'" limit 1'
                cursor = connection.cursor(buffered=True)
                cursor.execute(sqlTableExist)
                records = cursor.fetchone()
                
                cursor = connection.cursor(buffered=True)

                #Create new table command
                sqlCreateTable = "create table "+databaseTable+"(id INT NOT NULL AUTO_INCREMENT, no INT NOT NULL, name_of_chemicals TEXT NOT NULL, cabinets TEXT, cas_number TEXT, supplier TEXT NOT NULL, quantity TEXT NOT NULL, quantity_number INT NOT NULL, person TEXT NOT NULL, securitydata TEXT, input_date DATE, comment TEXT, PRIMARY KEY ( id ))"
                
                if(records is None): #Table not exist
                    cursor.execute(sqlCreateTable)
                else: #Table exist
                    #Drop old table
                    sqlDropTable = "drop table "+databaseTable
                    cursor.execute(sqlDropTable)

                    #Create new table
                    cursor.execute(sqlCreateTable)
                connection.commit() 
        except mysql.connector.Error as err:
            self.showMessage(msg, QMessageBox.Critical, "Fehler...", "Fehler "+str(err), "Fehler ")
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()  

        self.insertNewToDatabase(numberRowsTable)

    def isTableExists(self):
        try:
            connection = mysql.connector.connect(host=self.databaseHost,
                                                        database=database,
                                                        user=databaseUser,
                                                        password=databasePassword)
            if connection.is_connected:
                sqlTableExist = 'select * from information_schema.tables where table_schema="'+database+'" and table_name="'+databaseTable+'" limit 1'
                cursor = connection.cursor(buffered=True)
                cursor.execute(sqlTableExist)
                records = cursor.fetchone()

                if(records is None):
                    return False
                return True
        except mysql.connector.Error as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Fehler...")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Fehler")
            msg.exec_()
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()

    def createNewTable(self):
        try:
            connection = mysql.connector.connect(host=self.databaseHost,
                                                        database=database,
                                                        user=databaseUser,
                                                        password=databasePassword)
            sql = "create table "+databaseTable+"(id INT NOT NULL AUTO_INCREMENT, no INT NOT NULL, name_of_chemicals TEXT NOT NULL, cabinets TEXT, cas_number TEXT, supplier TEXT NOT NULL, quantity TEXT NOT NULL, quantity_number INT NOT NULL, person TEXT NOT NULL, securitydata TEXT, input_date DATE, comment TEXT, PRIMARY KEY ( id ))"
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit() 
        except mysql.connector.Error as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Fehler...")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Fehler")
            msg.exec_()
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()

    def insertDataToDatabase(self):
        box = QtWidgets.QMessageBox()
        box.setIcon(QtWidgets.QMessageBox.Question)
        box.setWindowTitle('Info')
        box.setText('Wollen Sie die neue Daten einfügen oder überschreiben?')
        box.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No|QtWidgets.QMessageBox.Cancel)
        buttonAdd = box.button(QtWidgets.QMessageBox.Yes)
        buttonAdd.setText('Einfügen')
        buttonOverwrite = box.button(QtWidgets.QMessageBox.No)
        buttonOverwrite.setText('Überschreiben')
        box.exec_()

        numberRowsTable = self.ui.tableWidget.rowCount()
        
        if box.clickedButton() == buttonAdd: #Add new data
            if(self.isTableExists()):
                lastNoInDatabase = self.getLastNoFromDatabase()
                self.insertNewToDatabase(numberRowsTable, lastNoInDatabase)
            else:
                boxAddNewTable = QtWidgets.QMessageBox()
                boxAddNewTable.setIcon(QtWidgets.QMessageBox.Question)
                boxAddNewTable.setWindowTitle('Info')
                boxAddNewTable.setText('Datentabelle existiert nicht! Wollen Sie neue Datentabelle einfügen?')
                boxAddNewTable.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
                buttonYes = boxAddNewTable.button(QtWidgets.QMessageBox.Yes)
                buttonYes.setText('Ja')
                buttonNein = boxAddNewTable.button(QtWidgets.QMessageBox.No)
                buttonNein.setText('Nein')
                boxAddNewTable.exec_()

                if boxAddNewTable.clickedButton() == buttonYes: #Add new table
                    self.createNewTable()
                    self.insertNewToDatabase(numberRowsTable)
        elif box.clickedButton() == buttonOverwrite: #Overwrite data
            self.overwriteNewDatabase(numberRowsTable)
        
        if self.window.show:
            self.window.close()
        
    def findStartRowStartCol(self, sheet):
        startRow = 0
        startCol = 0
        isTableFormCorrect = False

        for row in range(sheet.nrows):
            for col in range(sheet.ncols):
                if(sheet.cell_value(row, col) == strNo):
                    startRow = row + 1 #Skip header
                    startCol = col
                    #Check if table form correct
                    if(sheet.cell_value(row, col) == strNo and sheet.cell_value(row, col+1) == strNameChemicalsCol and sheet.cell_value(row, col+2) == strNameCASNumberCol and sheet.cell_value(row, col+3) == strSupplierCol and sheet.cell_value(row, col+4) == strQuantityCol and sheet.cell_value(row, col+5) == strQuantityAmountCol and sheet.cell_value(row, col+6) == strCommentCol):
                        isTableFormCorrect = True
                    break
                    
        return (startRow, startCol, isTableFormCorrect)

    def checkCommentForSetColor(self, comment):
        for elem in redMarkingCommentList:
            if(comment.find(elem) != -1):
                return True

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
        isNumberExistInComment = self.checkCommentForSetColor(comment)
        
        if(isNumberExistInComment):
            color = QtGui.QColor(255,0,0)
        else:
            color = QtGui.QColor(0,0,0,0)

        self.setBackgroundColor(tableRow, color)

    def insertDataToTable(self, sheet, startRow, startCol, tableRow, cabinnets):
        #Input person
        person = self.lePerson.text()
        today = self.dateEdit.text()

        for row in range(startRow, sheet.nrows):
            if(str(sheet.cell_value(row, startCol)) == ""): #name empty => pass
                continue
            else:
                self.ui.tableWidget.setItem(tableRow,noCol, QTableWidgetItem(str(tableRow+1)))
                self.ui.tableWidget.setItem(tableRow,nameChemicalsCol, QTableWidgetItem(str(sheet.cell_value(row, startCol+1))))
                #Save Row as key and Chemical name as value
                self.dictRowChemicalsName[tableRow] = str(sheet.cell_value(row, startCol+1))

                self.ui.tableWidget.setItem(tableRow,cabinetsCol, QTableWidgetItem(str(cabinnets)))

                self.ui.tableWidget.setItem(tableRow,casNumberCol, QTableWidgetItem(str(sheet.cell_value(row, startCol+2))))

                self.ui.tableWidget.setItem(tableRow,supplierCol, QTableWidgetItem(str(sheet.cell_value(row, startCol+3))))
                self.ui.tableWidget.setItem(tableRow,quantityCol, QTableWidgetItem(str(sheet.cell_value(row, startCol+4))))
                if(sheet.cell_value(row, startCol+5) == ""):
                    self.ui.tableWidget.setItem(tableRow,quantityAmountCol, QTableWidgetItem(str(0)))
                else:
                    self.ui.tableWidget.setItem(tableRow,quantityAmountCol, QTableWidgetItem(str(int(sheet.cell_value(row, startCol+5)))))
                self.ui.tableWidget.setItem(tableRow,personCol, QTableWidgetItem(person))
                self.ui.tableWidget.setItem(tableRow,securityDataCol, QTableWidgetItem(""))
                self.ui.tableWidget.setItem(tableRow,dateCol, QTableWidgetItem(today))
                self.ui.tableWidget.setItem(tableRow,commentCol, QTableWidgetItem(str(sheet.cell_value(row, startCol+6))))
                self.setBackgroundColorForCommentRow(tableRow, str(sheet.cell_value(row, startCol+6)))
                tableRow += 1
        
        return tableRow

if __name__ == "__main__":
    try:
        import sys
        app = QtWidgets.QApplication(sys.argv)
        myWindow = MyWindow()
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
