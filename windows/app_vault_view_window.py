import os
import sys
import pyperclip
import keyboard
import time
from threading import Thread
from pynput.mouse import Listener, Button

from PyQt5.QtWidgets import QDialog, QCheckBox, QToolButton, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, QThread, Qt

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

from workers.auto_type_worker import AutoType


class AppVaultView(Ui_AppVaultViewDialog, QDialog):
    previous_left = 0
    auto_type_thread_active = False
    def __init__(self, app):
        super(AppVaultView, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.app = app
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.set_icons()
        self.hideText()
        self.read_styles()
        
        self.lbl_name_view.setText(self.app[2])
        
        self.data = json_to_dict(self.app[3])
        
        # The widgets in the vertical layout are [0,2,4,6,8] because of the hlines
        self.chk_username.stateChanged.connect(lambda: self.show_hidden("username", self.chk_username, 1))
        self.chk_email.stateChanged.connect(lambda: self.show_hidden("email", self.chk_email, 3))
        self.chk_password.stateChanged.connect(lambda: self.show_hidden("password", self.chk_password, 5))
        self.chk_password_exp.stateChanged.connect(lambda: self.show_hidden("password_exp", self.chk_password_exp, 7))
        self.chk_twofa.stateChanged.connect(lambda: self.show_hidden("twofa_code", self.chk_twofa, 9))
        self.chk_path.stateChanged.connect(lambda: self.show_hidden("path", self.chk_path, 11))
        
        self.tbtn_username.clicked.connect(lambda: self.copy_data("username"))
        self.tbtn_email.clicked.connect(lambda: self.copy_data("email"))
        self.tbtn_password.clicked.connect(lambda: self.copy_data("password"))
        self.tbtn_password_exp.clicked.connect(lambda: self.copy_data("password_exp"))
        self.tbtn_twofa.clicked.connect(lambda: self.copy_data("twofa_code"))
        self.tbtn_path.clicked.connect(lambda: self.copy_data("path"))
        
        self.btn_open.clicked.connect(self.open_app)
        
    
    def read_styles(self):
        settings = Model().read('settings')[0]
        dark_mode_on = int(settings[1])
        checkbox = WhiteEyeCheckBox if dark_mode_on else BlackEyeCheckBox
        
        widget_list = [checkbox, Label, PushButton, RadioButton, Dialog, ToolButton]
        stylesheet = StyleSheet(widget_list).create()
        
        self.setStyleSheet(stylesheet)
        
        font_name = settings[2]
        
        font_widgets = [
            self.lbl_email,
            self.lbl_password,
            self.lbl_path,
            self.lbl_username,
            self.lbl_email_view,
            self.lbl_name_view,
            self.lbl_password_view,
            self.lbl_path_view,
            self.lbl_username_view,
            self.btn_open,
            self.lbl_password_exp,
            self.lbl_password_exp_view,
            self.lbl_twofa,
            self.lbl_twofa_view        
        ]
        
        widget: QWidget
        
        for widget in font_widgets:
            widget.setFont(QFont(font_name))
        
        
    def hideText(self):
        dots = u"\u2022"*10
        
        for i in range(1, self.layout().count() - 2, 2):
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
        if int(dark_mode_on):
            # Set the white copy icon
            icon = QIcon(":/input/copy_white")
        else:
            # Set the black copy icon
            icon = QIcon(":/input/copy_black")
        for i in range(1, self.layout().count() - 2, 2):
            tool_button: QToolButton = self.layout().itemAt(i).layout().itemAt(3).widget()
            tool_button.setIcon(icon)
            tool_button.setIconSize(QSize(25, 25))
        
    def open_app(self):
        os.startfile(self.data['path'])
        if not self.auto_type_thread_active:
            self.activate_auto_type()
             
    def activate_auto_type(self):
        things_to_type = [self.data['email'], self.data['password']]
        
        self.auto_type_thread = QThread()
        self.auto_typer = AutoType(things_to_type)
        
        self.auto_typer.moveToThread(self.auto_type_thread)
        
        # self.auto_typer.finished.connect(self.auto_type_thread_off)
        
        self.auto_type_thread.started.connect(self.auto_typer.auto_type)
        
        self.auto_typer.finished.connect(self.auto_typer.deleteLater)
        self.auto_type_thread.finished.connect(self.auto_type_off)
        
        self.auto_type_thread.start()
        self.auto_type_thread_active = True
        
    def auto_type_thread_off(self):
        self.auto_type_thread_active = False
        
    def auto_type_off(self):
        self.auto_type_thread.deleteLater
        self.auto_type_thread_active = False