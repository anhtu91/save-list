# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(988, 740)
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
        self.lbFraunhoferIcon.setPixmap(QtGui.QPixmap("fraunhofer_icon.jpg"))
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
        self.lbIPAddress.setText(_translate("MainWindow", "IP Adress von Server"))
        self.lbConnectionToDatabase.setText(_translate("MainWindow", "Verbindung mit Datenbank"))
        self.btnConnect.setText(_translate("MainWindow", "Verbinden"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
