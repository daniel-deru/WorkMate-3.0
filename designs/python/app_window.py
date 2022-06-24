# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './xml/app_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_App_Window(object):
    def setupUi(self, App_Window):
        App_Window.setObjectName("App_Window")
        App_Window.resize(514, 313)
        self.verticalLayout = QtWidgets.QVBoxLayout(App_Window)
        self.verticalLayout.setObjectName("verticalLayout")
        self.vbox_name = QtWidgets.QVBoxLayout()
        self.vbox_name.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.vbox_name.setSpacing(0)
        self.vbox_name.setObjectName("vbox_name")
        self.lbl_name = QtWidgets.QLabel(App_Window)
        self.lbl_name.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_name.sizePolicy().hasHeightForWidth())
        self.lbl_name.setSizePolicy(sizePolicy)
        self.lbl_name.setMinimumSize(QtCore.QSize(0, 20))
        self.lbl_name.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lbl_name.setObjectName("lbl_name")
        self.vbox_name.addWidget(self.lbl_name)
        self.lnedt_name = QtWidgets.QLineEdit(App_Window)
        self.lnedt_name.setObjectName("lnedt_name")
        self.vbox_name.addWidget(self.lnedt_name)
        self.verticalLayout.addLayout(self.vbox_name)
        self.vbox_index = QtWidgets.QVBoxLayout()
        self.vbox_index.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.vbox_index.setSpacing(0)
        self.vbox_index.setObjectName("vbox_index")
        self.lbl_index = QtWidgets.QLabel(App_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_index.sizePolicy().hasHeightForWidth())
        self.lbl_index.setSizePolicy(sizePolicy)
        self.lbl_index.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lbl_index.setObjectName("lbl_index")
        self.vbox_index.addWidget(self.lbl_index)
        self.spn_index = QtWidgets.QSpinBox(App_Window)
        self.spn_index.setObjectName("spn_index")
        self.vbox_index.addWidget(self.spn_index)
        self.verticalLayout.addLayout(self.vbox_index)
        self.vbox_path = QtWidgets.QVBoxLayout()
        self.vbox_path.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.vbox_path.setSpacing(0)
        self.vbox_path.setObjectName("vbox_path")
        self.lbl_path = QtWidgets.QLabel(App_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_path.sizePolicy().hasHeightForWidth())
        self.lbl_path.setSizePolicy(sizePolicy)
        self.lbl_path.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lbl_path.setObjectName("lbl_path")
        self.vbox_path.addWidget(self.lbl_path)
        self.lnedt_path = QtWidgets.QLineEdit(App_Window)
        self.lnedt_path.setObjectName("lnedt_path")
        self.vbox_path.addWidget(self.lnedt_path)
        self.verticalLayout.addLayout(self.vbox_path)
        self.hbox_desktop = QtWidgets.QHBoxLayout()
        self.hbox_desktop.setObjectName("hbox_desktop")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hbox_desktop.addItem(spacerItem)
        self.btn_desktop = QtWidgets.QPushButton(App_Window)
        self.btn_desktop.setMinimumSize(QtCore.QSize(200, 0))
        self.btn_desktop.setMaximumSize(QtCore.QSize(400, 16777215))
        self.btn_desktop.setObjectName("btn_desktop")
        self.hbox_desktop.addWidget(self.btn_desktop)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hbox_desktop.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.hbox_desktop)
        self.hbox_save = QtWidgets.QHBoxLayout()
        self.hbox_save.setObjectName("hbox_save")
        self.btn_discard = QtWidgets.QPushButton(App_Window)
        self.btn_discard.setObjectName("btn_discard")
        self.hbox_save.addWidget(self.btn_discard)
        self.btn_save = QtWidgets.QPushButton(App_Window)
        self.btn_save.setObjectName("btn_save")
        self.hbox_save.addWidget(self.btn_save)
        self.verticalLayout.addLayout(self.hbox_save)

        self.retranslateUi(App_Window)
        QtCore.QMetaObject.connectSlotsByName(App_Window)

    def retranslateUi(self, App_Window):
        _translate = QtCore.QCoreApplication.translate
        App_Window.setWindowTitle(_translate("App_Window", "Dialog"))
        self.lbl_name.setText(_translate("App_Window", "Name"))
        self.lbl_index.setText(_translate("App_Window", "Index"))
        self.lbl_path.setText(_translate("App_Window", "URL/Path"))
        self.btn_desktop.setText(_translate("App_Window", "Add From Desktop"))
        self.btn_discard.setText(_translate("App_Window", "Discard"))
        self.btn_save.setText(_translate("App_Window", "Save"))
