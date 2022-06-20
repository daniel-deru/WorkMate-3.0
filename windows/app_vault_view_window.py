from json import tool
import os
import sys
import pyperclip

from PyQt5.QtWidgets import QDialog, QCheckBox, QToolButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.app_vault_view_window import Ui_AppVaultViewDialog

from utils.helpers import StyleSheet, json_to_dict

from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton
from widgetStyles.RadioButton import RadioButton
from widgetStyles.QCheckBox import WhiteEyeCheckBox, BlackEyeCheckBox
from widgetStyles.Dialog import Dialog
from widgetStyles.ToolButton import ToolButton

from database.model import Model


class AppVaultView(Ui_AppVaultViewDialog, QDialog):
    def __init__(self, app):
        super(AppVaultView, self).__init__()
        self.app = app
        self.setupUi(self)
        self.set_icons()
        self.hideText()
        self.read_styles()
        
        self.data = json_to_dict(self.app[3])
        
        # The widgets in the vertical layout are [0,2,4,6,8] because of the hlines
        self.chk_name.stateChanged.connect(lambda: self.show_hidden("name", self.chk_name, 0))
        self.chk_username.stateChanged.connect(lambda: self.show_hidden("username", self.chk_username, 2))
        self.chk_email.stateChanged.connect(lambda: self.show_hidden("email", self.chk_email, 4))
        self.chk_password.stateChanged.connect(lambda: self.show_hidden("password", self.chk_password, 6))
        self.chk_path.stateChanged.connect(lambda: self.show_hidden("path", self.chk_path, 8))
        
        self.tbtn_name.clicked.connect(lambda: self.copy_data("name"))
        self.tbtn_username.clicked.connect(lambda: self.copy_data("username"))
        self.tbtn_email.clicked.connect(lambda: self.copy_data("email"))
        self.tbtn_password.clicked.connect(lambda: self.copy_data("password"))
        self.tbtn_path.clicked.connect(lambda: self.copy_data("path"))
        
        self.btn_open.clicked.connect(lambda: os.startfile(self.data['path']))
        
    
    def read_styles(self):
        dark_mode_on = Model().read('settings')[0][1]
        checkbox = WhiteEyeCheckBox if dark_mode_on else BlackEyeCheckBox
        
        widget_list = [checkbox, Label, PushButton, RadioButton, Dialog, ToolButton]
        stylesheet = StyleSheet(widget_list).create()
        
        self.setStyleSheet(stylesheet)
        
    def hideText(self):
        dots = u"\u2022"*10
        
        for i in range(0, self.layout().count() - 2, 2):
            self.layout().itemAt(i).layout().itemAt(1).widget().setText(dots)
        
    def show_hidden(self, field_name: str, checkbox: QCheckBox, label_index: int):
        label = self.layout().itemAt(label_index).layout().itemAt(1).widget()
        dots = u"\u2022"*10
        if checkbox.isChecked():
            label.setText(self.data[field_name])
        else:
            label.setText(dots)
            
    def copy_data(self, field_name: str):
        pyperclip.copy(self.data[field_name])
        
    def set_icons(self):
        dark_mode_on = Model().read('settings')[0][1]
        if dark_mode_on:
            # Set the white copy icon
            icon = QIcon("./assets/copy_white.svg")
        else:
            # Set the black copy icon
            icon = QIcon("./assets/copy_black.svg")
        for i in range(0, self.layout().count() - 2, 2):
            tool_button: QToolButton = self.layout().itemAt(i).layout().itemAt(3).widget()
            tool_button.setIcon(icon)
            tool_button.setIconSize(QSize(25, 25))