# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vault_tab.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Vault_tab(object):
    def setupUi(self, Vault_tab):
        Vault_tab.setObjectName("Vault_tab")
        Vault_tab.resize(524, 382)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Vault_tab.sizePolicy().hasHeightForWidth())
        Vault_tab.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Vault_tab)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hbox_login = QtWidgets.QHBoxLayout()
        self.hbox_login.setContentsMargins(0, 0, 0, 30)
        self.hbox_login.setSpacing(30)
        self.hbox_login.setObjectName("hbox_login")
        self.btn_login = QtWidgets.QPushButton(Vault_tab)
        self.btn_login.setObjectName("btn_login")
        self.hbox_login.addWidget(self.btn_login)
        self.btn_username = QtWidgets.QPushButton(Vault_tab)
        self.btn_username.setObjectName("btn_username")
        self.hbox_login.addWidget(self.btn_username)
        self.btn_password = QtWidgets.QPushButton(Vault_tab)
        self.btn_password.setObjectName("btn_password")
        self.hbox_login.addWidget(self.btn_password)
        self.verticalLayout.addLayout(self.hbox_login)
        self.tbl_vault = QtWidgets.QTableWidget(Vault_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbl_vault.sizePolicy().hasHeightForWidth())
        self.tbl_vault.setSizePolicy(sizePolicy)
        self.tbl_vault.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tbl_vault.setRowCount(0)
        self.tbl_vault.setObjectName("tbl_vault")
        self.tbl_vault.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_vault.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_vault.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_vault.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_vault.setHorizontalHeaderItem(3, item)
        self.tbl_vault.horizontalHeader().setVisible(True)
        self.tbl_vault.horizontalHeader().setCascadingSectionResizes(False)
        self.tbl_vault.verticalHeader().setHighlightSections(True)
        self.verticalLayout.addWidget(self.tbl_vault)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Vault_tab)
        QtCore.QMetaObject.connectSlotsByName(Vault_tab)

    def retranslateUi(self, Vault_tab):
        _translate = QtCore.QCoreApplication.translate
        Vault_tab.setWindowTitle(_translate("Vault_tab", "Form"))
        self.btn_login.setText(_translate("Vault_tab", "Login"))
        self.btn_username.setText(_translate("Vault_tab", "Show Username"))
        self.btn_password.setText(_translate("Vault_tab", "Show Password"))
        item = self.tbl_vault.horizontalHeaderItem(0)
        item.setText(_translate("Vault_tab", "Name"))
        item = self.tbl_vault.horizontalHeaderItem(1)
        item.setText(_translate("Vault_tab", "URL"))
        item = self.tbl_vault.horizontalHeaderItem(2)
        item.setText(_translate("Vault_tab", "Username"))
        item = self.tbl_vault.horizontalHeaderItem(3)
        item.setText(_translate("Vault_tab", "Password"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Vault_tab = QtWidgets.QWidget()
    ui = Ui_Vault_tab()
    ui.setupUi(Vault_tab)
    Vault_tab.show()
    sys.exit(app.exec_())
