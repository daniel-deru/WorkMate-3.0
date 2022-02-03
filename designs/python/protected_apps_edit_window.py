# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'protected_apps_edit_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProtectedAppsEdit(object):
    def setupUi(self, ProtectedAppsEdit):
        ProtectedAppsEdit.setObjectName("ProtectedAppsEdit")
        ProtectedAppsEdit.resize(475, 443)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(ProtectedAppsEdit)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.vbox_name = QtWidgets.QVBoxLayout()
        self.vbox_name.setObjectName("vbox_name")
        self.lbl_name = QtWidgets.QLabel(ProtectedAppsEdit)
        self.lbl_name.setObjectName("lbl_name")
        self.vbox_name.addWidget(self.lbl_name)
        self.lnedt_name = QtWidgets.QLineEdit(ProtectedAppsEdit)
        self.lnedt_name.setObjectName("lnedt_name")
        self.vbox_name.addWidget(self.lnedt_name)
        self.verticalLayout_7.addLayout(self.vbox_name)
        self.vbox_index = QtWidgets.QVBoxLayout()
        self.vbox_index.setObjectName("vbox_index")
        self.lbl_index = QtWidgets.QLabel(ProtectedAppsEdit)
        self.lbl_index.setObjectName("lbl_index")
        self.vbox_index.addWidget(self.lbl_index)
        self.spnbox_index = QtWidgets.QSpinBox(ProtectedAppsEdit)
        self.spnbox_index.setObjectName("spnbox_index")
        self.vbox_index.addWidget(self.spnbox_index)
        self.verticalLayout_7.addLayout(self.vbox_index)
        self.vbox_path = QtWidgets.QVBoxLayout()
        self.vbox_path.setObjectName("vbox_path")
        self.lbl_path = QtWidgets.QLabel(ProtectedAppsEdit)
        self.lbl_path.setObjectName("lbl_path")
        self.vbox_path.addWidget(self.lbl_path)
        self.lnedt_path = QtWidgets.QLineEdit(ProtectedAppsEdit)
        self.lnedt_path.setObjectName("lnedt_path")
        self.vbox_path.addWidget(self.lnedt_path)
        self.btn_desktop = QtWidgets.QPushButton(ProtectedAppsEdit)
        self.btn_desktop.setObjectName("btn_desktop")
        self.vbox_path.addWidget(self.btn_desktop)
        self.verticalLayout_7.addLayout(self.vbox_path)
        self.vbox_username = QtWidgets.QVBoxLayout()
        self.vbox_username.setObjectName("vbox_username")
        self.lbl_username = QtWidgets.QLabel(ProtectedAppsEdit)
        self.lbl_username.setObjectName("lbl_username")
        self.vbox_username.addWidget(self.lbl_username)
        self.lnedt_username = QtWidgets.QLineEdit(ProtectedAppsEdit)
        self.lnedt_username.setObjectName("lnedt_username")
        self.vbox_username.addWidget(self.lnedt_username)
        self.verticalLayout_7.addLayout(self.vbox_username)
        self.vbox_email = QtWidgets.QVBoxLayout()
        self.vbox_email.setObjectName("vbox_email")
        self.lbl_email = QtWidgets.QLabel(ProtectedAppsEdit)
        self.lbl_email.setObjectName("lbl_email")
        self.vbox_email.addWidget(self.lbl_email)
        self.lnedt_email = QtWidgets.QLineEdit(ProtectedAppsEdit)
        self.lnedt_email.setObjectName("lnedt_email")
        self.vbox_email.addWidget(self.lnedt_email)
        self.verticalLayout_7.addLayout(self.vbox_email)
        self.vbox_password = QtWidgets.QVBoxLayout()
        self.vbox_password.setObjectName("vbox_password")
        self.lbl_password = QtWidgets.QLabel(ProtectedAppsEdit)
        self.lbl_password.setObjectName("lbl_password")
        self.vbox_password.addWidget(self.lbl_password)
        self.lnedt_password = QtWidgets.QLineEdit(ProtectedAppsEdit)
        self.lnedt_password.setObjectName("lnedt_password")
        self.vbox_password.addWidget(self.lnedt_password)
        self.verticalLayout_7.addLayout(self.vbox_password)
        self.hbox_save = QtWidgets.QHBoxLayout()
        self.hbox_save.setObjectName("hbox_save")
        self.btn_discard = QtWidgets.QPushButton(ProtectedAppsEdit)
        self.btn_discard.setObjectName("btn_discard")
        self.hbox_save.addWidget(self.btn_discard)
        self.btn_save = QtWidgets.QPushButton(ProtectedAppsEdit)
        self.btn_save.setObjectName("btn_save")
        self.hbox_save.addWidget(self.btn_save)
        self.verticalLayout_7.addLayout(self.hbox_save)

        self.retranslateUi(ProtectedAppsEdit)
        QtCore.QMetaObject.connectSlotsByName(ProtectedAppsEdit)

    def retranslateUi(self, ProtectedAppsEdit):
        _translate = QtCore.QCoreApplication.translate
        ProtectedAppsEdit.setWindowTitle(_translate("ProtectedAppsEdit", "Edit Protected Apps"))
        self.lbl_name.setText(_translate("ProtectedAppsEdit", "Name"))
        self.lbl_index.setText(_translate("ProtectedAppsEdit", "Index"))
        self.lbl_path.setText(_translate("ProtectedAppsEdit", "URL/Path"))
        self.btn_desktop.setText(_translate("ProtectedAppsEdit", "Choose From Desktop"))
        self.lbl_username.setText(_translate("ProtectedAppsEdit", "Username"))
        self.lbl_email.setText(_translate("ProtectedAppsEdit", "Email"))
        self.lbl_password.setText(_translate("ProtectedAppsEdit", "Password"))
        self.btn_discard.setText(_translate("ProtectedAppsEdit", "Discard"))
        self.btn_save.setText(_translate("ProtectedAppsEdit", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ProtectedAppsEdit = QtWidgets.QDialog()
    ui = Ui_ProtectedAppsEdit()
    ui.setupUi(ProtectedAppsEdit)
    ProtectedAppsEdit.show()
    sys.exit(app.exec_())