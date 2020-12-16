# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'database.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class uiDatabaseWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1225, 721)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(2, 100, 1221, 531))
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(390, 10, 511, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.btnDelete = QtWidgets.QPushButton(self.centralwidget)
        self.btnDelete.setGeometry(QtCore.QRect(790, 640, 211, 51))
        self.btnDelete.setObjectName("btnDelete")
        self.btnEditSave = QtWidgets.QPushButton(self.centralwidget)
        self.btnEditSave.setGeometry(QtCore.QRect(1010, 640, 211, 51))
        self.btnEditSave.setObjectName("btnEditSave")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(620, 56, 603, 41))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.widget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.btnSearch = QtWidgets.QPushButton(self.splitter)
        self.btnSearch.setObjectName("btnSearch")
        self.teSearch = QtWidgets.QTextEdit(self.splitter)
        self.teSearch.setObjectName("teSearch")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.teSearch.setFont(font)
        self.horizontalLayout.addWidget(self.splitter)
        self.splitter_2 = QtWidgets.QSplitter(self.widget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.lbSort = QtWidgets.QLabel(self.splitter_2)
        self.lbSort.setObjectName("lbSort")
        self.cbSort = QtWidgets.QComboBox(self.splitter_2)
        self.cbSort.setObjectName("cbSort")
        self.horizontalLayout.addWidget(self.splitter_2)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(4, 650, 161, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1225, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Datenbank"))
        self.label.setText(_translate("MainWindow", "Speicherte List von Chemikals des Batterielabors CL25"))
        self.btnDelete.setText(_translate("MainWindow", "Löschen selectiert Zeil"))
        self.btnEditSave.setText(_translate("MainWindow", "Speichern"))
        self.btnSearch.setText(_translate("MainWindow", "Suchen"))
        self.lbSort.setText(_translate("MainWindow", "Sortiert Schrank"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#cc0000;\">Rot Farbe: Giftstoff</span></p></body></html>"))

