# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ie.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


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
        self.lbFraunhoferIcon.setPixmap(QtGui.QPixmap("fraunhofer_icon.jpg"))
        self.lbFraunhoferIcon.setObjectName("lbFraunhoferIcon")
        self.horizontalLayout_2.addWidget(self.lbFraunhoferIcon)
        self.lbContact = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ImportExport = QtWidgets.QMainWindow()
    ui = Ui_ImportExport()
    ui.setupUi(ImportExport)
    ImportExport.show()
    sys.exit(app.exec_())
