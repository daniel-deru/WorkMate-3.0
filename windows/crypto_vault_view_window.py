import sys
import os
import math
from turtle import dot
import pyperclip

from PyQt5.QtWidgets import (
    QDialog, 
    QLabel, 
    QHBoxLayout, 
    QToolButton,
    QCheckBox, 
    QFrame, 
    QSpacerItem, 
    QSizePolicy,
    QWidget
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCursor, QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.ToolButton import ToolButton
from widgetStyles.PushButton import PushButton
from widgetStyles.Dialog import Dialog
from widgetStyles.QCheckBox import BlackEyeCheckBox, WhiteEyeCheckBox

from utils.helpers import StyleSheet, json_to_dict
from utils.message import Message

from designs.python.crypto_vault_view_window import Ui_CryptoViewWindow

from database.model import Model

from windows.login_window import Login

class CryptoVaultViewWindow(Ui_CryptoViewWindow, QDialog):
    def __init__(self, secret):
        super(CryptoVaultViewWindow, self).__init__()
        self.secret = secret
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.data = json_to_dict(self.secret[3])
        self.settings = Model().read("settings")[0]
        self.night_mode_on: int = int(self.settings[1])
        self.font_name = self.settings[2]
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.read_styles()
        self.set_dots()
        self.set_data()
        self.set_icons()
        
        
        self.tbtn_username.clicked.connect(lambda: self.copy("name"))
        self.tbtn_password.clicked.connect(lambda: self.copy("password"))
        self.tbtn_public.clicked.connect(lambda: self.copy("public_key"))
        self.tbtn_private.clicked.connect(lambda: self.private_login(self.tbtn_private))
        self.tbtn_password_exp.clicked.connect(lambda: self.copy("password_exp"))
        
        self.chk_username.stateChanged.connect(lambda: self.view("name", self.lbl_username, self.chk_username))
        self.chk_password.stateChanged.connect(lambda: self.view("password", self.lbl_password, self.chk_password))
        self.chk_public.stateChanged.connect(lambda: self.view("public_key", self.lbl_public, self.chk_public))
        self.chk_password_exp.stateChanged.connect(lambda: self.view("password_exp", self.lbl_password_exp, self.chk_password_exp))
        self.chk_private.stateChanged.connect(lambda: self.private_login(self.chk_private))        
        
    def read_styles(self):
        settings = Model().read("settings")[0]
        night_mode_on: int = int(settings[1])
        
        checkbox = WhiteEyeCheckBox if night_mode_on else BlackEyeCheckBox
        widget_list = [
            checkbox,
            Label,
            LineEdit,
            ToolButton,
            PushButton,
            Dialog
        ]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_name = settings[2]
        
        font_widgets = [
            self.btn_copyall,
            self.lbl_description,
            self.lbl_password,
            self.lbl_private,
            self.lbl_public,
            self.lbl_username,
            self.lbl_password_view,
            self.lbl_private_view,
            self.lbl_public_view,
            self.lbl_username_view,
            self.lbl_password_exp,
            self.lbl_password_exp_view,
            self.btn_delete,
            self.btn_edit
        ]

        widget: QWidget
        
        for widget in font_widgets:
            widget.setFont(QFont(font_name))
        
        
        
        
    def set_data(self):
        self.lbl_description.setText(self.data['description'])
        
        words: list[str] = self.data['words'].split(" ")
        COLUMNS = 3
        count = 1
        for i in range(math.ceil(len(words)/COLUMNS)):
            for j in range(COLUMNS):
                frame = self.create_word_boxes(count, words[count - 1])
                self.gbox_words.addWidget(frame, i, j)
                count += 1
        
    def set_dots(self):
        dots = u"\u2022"*10
        self.lbl_username.setText(dots)
        self.lbl_password.setText(dots)
        self.lbl_private.setText(dots)
        self.lbl_public.setText(dots)
        self.lbl_password_exp.setText(dots)

    def set_icons(self):
                
        icon_path: str = ":/input/copy_white" if self.night_mode_on else ":/input/copy_black"
        icon: QIcon = QIcon(icon_path)
        
        button_list = [
            self.tbtn_password,
            self.tbtn_private,
            self.tbtn_username,
            self.tbtn_public,
            self.tbtn_password_exp
        ]
        
        for button in button_list:
            button: QToolButton
            button.setIcon(icon)
            button.setIconSize(QSize(20, 20))
        
    def create_word_boxes(self, count: int, word: str) -> QFrame:
        hbox = QHBoxLayout()
        tool_button_icon_path = "./assets/copy_white.svg" if self.night_mode_on else "./assets/copy_black.svg"
        icon = QIcon(tool_button_icon_path)
        
        num = QLabel(f"{str(count).zfill(2)} ")
        num.setFont(QFont(self.font_name))
        num.setFixedWidth(30)
        num_color = "#9ecd16" if self.night_mode_on else "#FF4400"
        num.setStyleSheet(f"color: {num_color};")
        
        lbl_word = QLabel(u"\u2022"*10)
        lbl_word.setFont(QFont(self.font_name))
        lbl_word.setMinimumWidth(100)
        
        copy = QToolButton()
        copy.setIcon(icon)
        copy.setIconSize(QSize(20, 20))
        copy.setCursor(QCursor(Qt.PointingHandCursor))
        copy.clicked.connect(lambda: self.copy_word(word))
        
        view = QCheckBox()
        view.setCursor(QCursor(Qt.PointingHandCursor))
        view.stateChanged.connect(lambda: self.view_word(word, view, lbl_word))
        
        hspacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        hbox.addWidget(num)
        hbox.addWidget(lbl_word)
        hbox.addItem(hspacer)
        hbox.addWidget(copy)
        hbox.addWidget(view)
        
        frame: QFrame = QFrame()
        frame.setObjectName("view_frame")
        frame.setStyleSheet("QFrame#view_frame{border: 2px solid #005BC6;border-radius: 5px;}")
        frame.setLayout(hbox)
        
        return frame
    
    def copy(self, field_name: str):
        try:
            pyperclip.copy(self.data[field_name])
        except KeyError:
            pass
        
    def view(self, field_name, label, checkbox):
        if checkbox.isChecked():
            try:
                label.setText(self.data[field_name])
            except KeyError:
                Message("There is no public key.", "No public key").exec_()
                checkbox.setChecked(False)
                checkbox.setCheckState(Qt.Unchecked)
        else:
            label.setText(u"\u2022"*10)
            
    def copy_word(self, word: str):
        pyperclip.copy(word)
        
    def view_word(self, word, checkbox, label):
        if checkbox.isChecked():
            label.setText(word)
        else:
            label.setText(u"\u2022"*10)
            
    def private_login(self, widget):
        if type(widget) == QCheckBox and not widget.isChecked():
            self.lbl_private.setText(u"\u2022"*10)
        else:
            if not "private_key" in self.data:
                Message("There is no private key.", "No private key").exec_()
                if type(widget) == QCheckBox:
                    widget.setChecked(False)
                    widget.setCheckState(Qt.Unchecked)
            else:
                login_window = Login()
                login_window.login_status.connect(lambda s: self.show_private(s, widget))
                login_window.exec_()
        
    def show_private(self, status, widget):
        if status == "success":
            if type(widget) is QToolButton:
                pyperclip.copy(self.data['private_key'])
            else:
                widget.setChecked(True)
                # widget.setCheckState(Qt.Checked)
                self.lbl_private.setText(self.data['private_key'])
        elif status == "failure" and type(widget) is QCheckBox:
            widget.setChecked(False)
            widget.setCheckState(Qt.Unchecked)
        