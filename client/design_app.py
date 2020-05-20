# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_app.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(821, 551)
        MainWindow.setFocusPolicy(QtCore.Qt.WheelFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 801, 481))
        self.textBrowser.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.textBrowser.setObjectName("textBrowser")
        self.inputMessage = QtWidgets.QLineEdit(self.centralwidget)
        self.inputMessage.setGeometry(QtCore.QRect(10, 500, 651, 41))
        self.inputMessage.setObjectName("inputMessage")
        self.btnSend = QtWidgets.QPushButton(self.centralwidget)
        self.btnSend.setGeometry(QtCore.QRect(670, 500, 141, 41))
        self.btnSend.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnSend.setObjectName("btnSend")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RSA Messenger"))
        self.btnSend.setText(_translate("MainWindow", "Send"))
