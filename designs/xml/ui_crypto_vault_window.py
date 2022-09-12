# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\SA Trust PC Big\Desktop\WorkMate 3.0 Pro\designs\xml\crypto_vault_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CryptoVault(object):
    def setupUi(self, CryptoVault):
        CryptoVault.setObjectName("CryptoVault")
        CryptoVault.resize(614, 322)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(CryptoVault)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.lbl_generate_password = QtWidgets.QLabel(CryptoVault)
        self.lbl_generate_password.setObjectName("lbl_generate_password")
        self.horizontalLayout_3.addWidget(self.lbl_generate_password)
        self.tbtn_generate_password = QtWidgets.QToolButton(CryptoVault)
        self.tbtn_generate_password.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tbtn_generate_password.setText("")
        self.tbtn_generate_password.setObjectName("tbtn_generate_password")
        self.horizontalLayout_3.addWidget(self.tbtn_generate_password)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.lbl_description = QtWidgets.QLabel(CryptoVault)
        self.lbl_description.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_description.setObjectName("lbl_description")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_description)
        self.lne_description = QtWidgets.QLineEdit(CryptoVault)
        self.lne_description.setObjectName("lne_description")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lne_description)
        self.lbl_words = QtWidgets.QLabel(CryptoVault)
        self.lbl_words.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_words.setObjectName("lbl_words")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_words)
        self.lbl_name = QtWidgets.QLabel(CryptoVault)
        self.lbl_name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_name.setObjectName("lbl_name")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lbl_name)
        self.lne_name = QtWidgets.QLineEdit(CryptoVault)
        self.lne_name.setObjectName("lne_name")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lne_name)
        self.lbl_password = QtWidgets.QLabel(CryptoVault)
        self.lbl_password.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_password.setObjectName("lbl_password")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lbl_password)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lne_password1 = QtWidgets.QLineEdit(CryptoVault)
        self.lne_password1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lne_password1.setObjectName("lne_password1")
        self.horizontalLayout_4.addWidget(self.lne_password1)
        self.chk_password1 = QtWidgets.QCheckBox(CryptoVault)
        self.chk_password1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chk_password1.setText("")
        self.chk_password1.setObjectName("chk_password1")
        self.horizontalLayout_4.addWidget(self.chk_password1)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.lbl_password2 = QtWidgets.QLabel(CryptoVault)
        self.lbl_password2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_password2.setObjectName("lbl_password2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.lbl_password2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lne_password2 = QtWidgets.QLineEdit(CryptoVault)
        self.lne_password2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lne_password2.setObjectName("lne_password2")
        self.horizontalLayout_5.addWidget(self.lne_password2)
        self.chk_password2 = QtWidgets.QCheckBox(CryptoVault)
        self.chk_password2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chk_password2.setText("")
        self.chk_password2.setObjectName("chk_password2")
        self.horizontalLayout_5.addWidget(self.chk_password2)
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.lbl_public = QtWidgets.QLabel(CryptoVault)
        self.lbl_public.setObjectName("lbl_public")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.lbl_public)
        self.lbl_private = QtWidgets.QLabel(CryptoVault)
        self.lbl_private.setObjectName("lbl_private")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.lbl_private)
        self.lne_public = QtWidgets.QLineEdit(CryptoVault)
        self.lne_public.setObjectName("lne_public")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.lne_public)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lne_private = QtWidgets.QLineEdit(CryptoVault)
        self.lne_private.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lne_private.setObjectName("lne_private")
        self.horizontalLayout.addWidget(self.lne_private)
        self.chk_private_key = QtWidgets.QCheckBox(CryptoVault)
        self.chk_private_key.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chk_private_key.setText("")
        self.chk_private_key.setObjectName("chk_private_key")
        self.horizontalLayout.addWidget(self.chk_private_key)
        self.formLayout.setLayout(8, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.lbl_password_exp = QtWidgets.QLabel(CryptoVault)
        self.lbl_password_exp.setObjectName("lbl_password_exp")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.lbl_password_exp)
        self.dte_password_exp = QtWidgets.QDateEdit(CryptoVault)
        self.dte_password_exp.setCalendarPopup(True)
        self.dte_password_exp.setObjectName("dte_password_exp")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.dte_password_exp)
        self.lbl_group = QtWidgets.QLabel(CryptoVault)
        self.lbl_group.setObjectName("lbl_group")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.lbl_group)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.cmb_num_words = QtWidgets.QComboBox(CryptoVault)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmb_num_words.sizePolicy().hasHeightForWidth())
        self.cmb_num_words.setSizePolicy(sizePolicy)
        self.cmb_num_words.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cmb_num_words.setObjectName("cmb_num_words")
        self.cmb_num_words.addItem("")
        self.cmb_num_words.addItem("")
        self.cmb_num_words.addItem("")
        self.cmb_num_words.addItem("")
        self.cmb_num_words.addItem("")
        self.horizontalLayout_6.addWidget(self.cmb_num_words)
        self.tbtn_num_words = QtWidgets.QToolButton(CryptoVault)
        self.tbtn_num_words.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tbtn_num_words.setObjectName("tbtn_num_words")
        self.horizontalLayout_6.addWidget(self.tbtn_num_words)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.cmb_group = QtWidgets.QComboBox(CryptoVault)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmb_group.sizePolicy().hasHeightForWidth())
        self.cmb_group.setSizePolicy(sizePolicy)
        self.cmb_group.setObjectName("cmb_group")
        self.horizontalLayout_7.addWidget(self.cmb_group)
        self.tbtn_add_group = QtWidgets.QToolButton(CryptoVault)
        self.tbtn_add_group.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tbtn_add_group.setObjectName("tbtn_add_group")
        self.horizontalLayout_7.addWidget(self.tbtn_add_group)
        self.formLayout.setLayout(5, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_7)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_save = QtWidgets.QPushButton(CryptoVault)
        self.btn_save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_2.addWidget(self.btn_save)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(CryptoVault)
        QtCore.QMetaObject.connectSlotsByName(CryptoVault)

    def retranslateUi(self, CryptoVault):
        _translate = QtCore.QCoreApplication.translate
        CryptoVault.setWindowTitle(_translate("CryptoVault", "Add Crypto Secret"))
        self.lbl_generate_password.setText(_translate("CryptoVault", "Password Generator"))
        self.lbl_description.setText(_translate("CryptoVault", "Description"))
        self.lbl_words.setText(_translate("CryptoVault", "Number of Words"))
        self.lbl_name.setText(_translate("CryptoVault", "Username"))
        self.lbl_password.setText(_translate("CryptoVault", "Password"))
        self.lbl_password2.setText(_translate("CryptoVault", "Confirm Password"))
        self.lbl_public.setText(_translate("CryptoVault", "Public Key (optional)"))
        self.lbl_private.setText(_translate("CryptoVault", "Private Key (optional)"))
        self.lbl_password_exp.setText(_translate("CryptoVault", "Password Expiration"))
        self.lbl_group.setText(_translate("CryptoVault", "Group"))
        self.cmb_num_words.setItemText(0, _translate("CryptoVault", "12 Words"))
        self.cmb_num_words.setItemText(1, _translate("CryptoVault", "15 Words"))
        self.cmb_num_words.setItemText(2, _translate("CryptoVault", "18 Words"))
        self.cmb_num_words.setItemText(3, _translate("CryptoVault", "21 Words"))
        self.cmb_num_words.setItemText(4, _translate("CryptoVault", "24 Words"))
        self.tbtn_num_words.setText(_translate("CryptoVault", "Add"))
        self.tbtn_add_group.setText(_translate("CryptoVault", "Add"))
        self.btn_save.setText(_translate("CryptoVault", "Save"))
