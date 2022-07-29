# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './xml/2fa_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TwoFADialog(object):
    def setupUi(self, TwoFADialog):
        TwoFADialog.setObjectName("TwoFADialog")
        TwoFADialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(TwoFADialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_message = QtWidgets.QLabel(TwoFADialog)
        self.lbl_message.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_message.setObjectName("lbl_message")
        self.verticalLayout.addWidget(self.lbl_message)
        self.lbl_qrcode = QtWidgets.QLabel(TwoFADialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_qrcode.sizePolicy().hasHeightForWidth())
        self.lbl_qrcode.setSizePolicy(sizePolicy)
        self.lbl_qrcode.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_qrcode.setObjectName("lbl_qrcode")
        self.verticalLayout.addWidget(self.lbl_qrcode)
        self.lbl_setupkey = QtWidgets.QLabel(TwoFADialog)
        self.lbl_setupkey.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_setupkey.setObjectName("lbl_setupkey")
        self.verticalLayout.addWidget(self.lbl_setupkey)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_copy = QtWidgets.QPushButton(TwoFADialog)
        self.btn_copy.setObjectName("btn_copy")
        self.horizontalLayout.addWidget(self.btn_copy)
        self.btn_exit = QtWidgets.QPushButton(TwoFADialog)
        self.btn_exit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_exit.setObjectName("btn_exit")
        self.horizontalLayout.addWidget(self.btn_exit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TwoFADialog)
        QtCore.QMetaObject.connectSlotsByName(TwoFADialog)

    def retranslateUi(self, TwoFADialog):
        _translate = QtCore.QCoreApplication.translate
        TwoFADialog.setWindowTitle(_translate("TwoFADialog", "Two Factor Authentication Setup"))
        self.lbl_message.setText(_translate("TwoFADialog", "Scan the QR code below or enter the setup key below the QR code."))
        self.lbl_qrcode.setText(_translate("TwoFADialog", "QR Code"))
        self.lbl_setupkey.setText(_translate("TwoFADialog", "Setup Key"))
        self.btn_copy.setText(_translate("TwoFADialog", "Copy"))
        self.btn_exit.setText(_translate("TwoFADialog", "Exit"))
