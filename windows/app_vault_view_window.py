import os
import sys

from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QToolButton, QHBoxLayout, QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QIcon


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.app_vault_view_window import Ui_AppVaultViewDialog

from utils.helpers import StyleSheet

from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton
from widgetStyles.RadioButton import RadioButton
from widgetStyles.QCheckBox import CheckBox
from widgetStyles.Dialog import Dialog


class AppVaultView(Ui_AppVaultViewDialog, QDialog):
    def __init__(self, app):
        super(AppVaultView, self).__init__()
        self.app = app
        self.setupUi(self)
        self.hideText()
        self.read_styles()
        
        self.chk_name.stateChanged.connect(lambda: self.show_hidden("name"))
        self.chk_username.stateChanged.connect(lambda: self.show_hidden("username"))
        self.chk_password.stateChanged.connect(lambda: self.show_hidden("password"))
        self.chk_email.stateChanged.connect(lambda: self.show_hidden("email"))
        self.chk_path.stateChanged.connect(lambda: self.show_hidden("path"))
        
        for i in range(0, self.layout().count() - 2, 2):
            print(self.layout().itemAt(i).layout().itemAt(0).widget().text())
            print(i)
    
    def read_styles(self):
        widget_list = [CheckBox, Label, PushButton, RadioButton, Dialog]
        stylesheet = StyleSheet(widget_list).create()
        
        self.setStyleSheet(stylesheet)
        
    def hideText(self):
        dots = u"\u2022"*10
        # self.lbl_name.setText(dots)
        # self.lbl_email.setText(dots)
        # self.lbl_username.setText(dots)
        # self.lbl_path.setText(dots)
        # self.lbl_password.setText(dots)
        
        for i in range(0, self.layout().count() - 2, 2):
            print(self.layout().itemAt(i).layout().itemAt(1).widget().setText(dots))
            # print(i)
        
    def show_hidden(self, field_name):
        print(field_name)
        