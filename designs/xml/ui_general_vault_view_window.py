# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\SA Trust PC Big\Desktop\WorkMate 3.0 Pro\designs\xml\general_vault_view_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GeneralVaultView(object):
    def setupUi(self, GeneralVaultView):
        GeneralVaultView.setObjectName("GeneralVaultView")
        GeneralVaultView.resize(621, 76)
        self.verticalLayout = QtWidgets.QVBoxLayout(GeneralVaultView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_description = QtWidgets.QLabel(GeneralVaultView)
        self.lbl_description.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_description.setObjectName("lbl_description")
        self.verticalLayout.addWidget(self.lbl_description)
        self.vbox_secrets = QtWidgets.QVBoxLayout()
        self.vbox_secrets.setObjectName("vbox_secrets")
        self.verticalLayout.addLayout(self.vbox_secrets)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_edit = QtWidgets.QPushButton(GeneralVaultView)
        self.btn_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_edit.setObjectName("btn_edit")
        self.horizontalLayout.addWidget(self.btn_edit)
        self.btn_delete = QtWidgets.QPushButton(GeneralVaultView)
        self.btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout.addWidget(self.btn_delete)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(GeneralVaultView)
        QtCore.QMetaObject.connectSlotsByName(GeneralVaultView)

    def retranslateUi(self, GeneralVaultView):
        _translate = QtCore.QCoreApplication.translate
        GeneralVaultView.setWindowTitle(_translate("GeneralVaultView", "View Vault"))
        self.lbl_description.setText(_translate("GeneralVaultView", "TextLabel"))
        self.btn_edit.setText(_translate("GeneralVaultView", "Edit"))
        self.btn_delete.setText(_translate("GeneralVaultView", "Delete"))
