# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './xml/login_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(400, 90)
        self.verticalLayout = QtWidgets.QVBoxLayout(Login)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_password = QtWidgets.QLabel(Login)
        self.lbl_password.setObjectName("lbl_password")
        self.verticalLayout.addWidget(self.lbl_password)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lnedt_password = QtWidgets.QLineEdit(Login)
        self.lnedt_password.setObjectName("lnedt_password")
        self.horizontalLayout_2.addWidget(self.lnedt_password)
        self.chk_show_password = QtWidgets.QCheckBox(Login)
        self.chk_show_password.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chk_show_password.setText("")
        self.chk_show_password.setObjectName("chk_show_password")
        self.horizontalLayout_2.addWidget(self.chk_show_password)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_login = QtWidgets.QPushButton(Login)
        self.btn_login.setObjectName("btn_login")
        self.horizontalLayout.addWidget(self.btn_login)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Login"))
        self.lbl_password.setText(_translate("Login", "Enter Your Password"))
        self.btn_login.setText(_translate("Login", "Login"))
