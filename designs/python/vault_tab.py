# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './xml/vault_tab.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Vault_tab(object):
    def setupUi(self, Vault_tab):
        Vault_tab.setObjectName("Vault_tab")
        Vault_tab.resize(640, 382)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Vault_tab.sizePolicy().hasHeightForWidth())
        Vault_tab.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Vault_tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hbox_controls = QtWidgets.QHBoxLayout()
        self.hbox_controls.setObjectName("hbox_controls")
        self.hbox_filter_widget = QtWidgets.QHBoxLayout()
        self.hbox_filter_widget.setObjectName("hbox_filter_widget")
        self.hbox_controls.addLayout(self.hbox_filter_widget)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hbox_controls.addItem(spacerItem)
        self.chk_edit = QtWidgets.QCheckBox(Vault_tab)
        self.chk_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chk_edit.setObjectName("chk_edit")
        self.hbox_controls.addWidget(self.chk_edit)
        self.btn_delete = QtWidgets.QPushButton(Vault_tab)
        self.btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete.setObjectName("btn_delete")
        self.hbox_controls.addWidget(self.btn_delete)
        self.btn_add = QtWidgets.QPushButton(Vault_tab)
        self.btn_add.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add.setObjectName("btn_add")
        self.hbox_controls.addWidget(self.btn_add)
        self.btn_login = QtWidgets.QPushButton(Vault_tab)
        self.btn_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_login.setObjectName("btn_login")
        self.hbox_controls.addWidget(self.btn_login)
        self.verticalLayout.addLayout(self.hbox_controls)
        self.lbl_secret = QtWidgets.QLabel(Vault_tab)
        self.lbl_secret.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_secret.setObjectName("lbl_secret")
        self.verticalLayout.addWidget(self.lbl_secret)
        self.line = QtWidgets.QFrame(Vault_tab)
        self.line.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line.setStyleSheet("background: #9ecd16;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.scrollArea = QtWidgets.QScrollArea(Vault_tab)
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 622, 307))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gbox_secrets = QtWidgets.QGridLayout()
        self.gbox_secrets.setObjectName("gbox_secrets")
        self.verticalLayout_2.addLayout(self.gbox_secrets)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Vault_tab)
        QtCore.QMetaObject.connectSlotsByName(Vault_tab)

    def retranslateUi(self, Vault_tab):
        _translate = QtCore.QCoreApplication.translate
        Vault_tab.setWindowTitle(_translate("Vault_tab", "Form"))
        self.chk_edit.setText(_translate("Vault_tab", "Edit"))
        self.btn_delete.setText(_translate("Vault_tab", "Delete"))
        self.btn_add.setText(_translate("Vault_tab", "Add"))
        self.btn_login.setText(_translate("Vault_tab", "Login"))
        self.lbl_secret.setText(_translate("Vault_tab", "Vault Items"))
