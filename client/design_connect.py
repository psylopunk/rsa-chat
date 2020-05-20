# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_connect.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(339, 144)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnConnect = QtWidgets.QPushButton(self.centralwidget)
        self.btnConnect.setGeometry(QtCore.QRect(200, 90, 131, 31))
        self.btnConnect.setObjectName("btnConnect")
        self.inputBox = QtWidgets.QLineEdit(self.centralwidget)
        self.inputBox.setGeometry(QtCore.QRect(20, 10, 311, 31))
        self.inputBox.setObjectName("inputBox")
        self.inputName = QtWidgets.QLineEdit(self.centralwidget)
        self.inputName.setGeometry(QtCore.QRect(20, 50, 311, 31))
        self.inputName.setObjectName("inputName")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Connect"))
        self.btnConnect.setText(_translate("MainWindow", "Войти"))
        self.inputBox.setPlaceholderText(_translate("MainWindow", "Box"))
        self.inputName.setPlaceholderText(_translate("MainWindow", "Name"))
