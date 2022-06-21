import json
import sys
import os
import math
from PyQt5.QtWidgets import QDialog, QLabel, QHBoxLayout, QToolButton, QCheckBox, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.ToolButton import ToolButton
from widgetStyles.PushButton import PushButton
from widgetStyles.Dialog import Dialog
from widgetStyles.QCheckBox import BlackEyeCheckBox, WhiteEyeCheckBox

from utils.helpers import StyleSheet, json_to_dict

from designs.python.crypto_vault_view_window import Ui_CryptoViewWindow

from database.model import Model

class CryptoVaultViewWindow(Ui_CryptoViewWindow, QDialog):
    def __init__(self, secret):
        super(CryptoVaultViewWindow, self).__init__()
        self.secret = secret
        self.data = json_to_dict(self.secret[3])
        self.night_mode_on: int = Model().read("settings")[0][1]
        self.setupUi(self)
        self.read_styles()
        self.set_dots()
        self.set_data()
        self.set_icons()
        
        
        
    def read_styles(self):
        night_mode_on: int = Model().read("settings")[0][1]
        
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

    def set_icons(self):
        night_mode_on: int = Model().read("settings")[0][1]
        
        icon_path: str = "./assets/copy_white.svg" if self.night_mode_on else "./assets/copy_black.svg"
        icon: QIcon = QIcon(icon_path)
        
        self.tbtn_password.setIcon(icon)
        self.tbtn_password.setIconSize(QSize(20, 20))
        self.tbtn_private.setIcon(icon)
        self.tbtn_private.setIconSize(QSize(20, 20))
        self.tbtn_username.setIcon(icon)
        self.tbtn_username.setIconSize(QSize(20, 20))
        self.tbtn_public.setIcon(icon)
        self.tbtn_public.setIconSize(QSize(20, 20))
        
    def create_word_boxes(self, count: int, word: str) -> QFrame:
        hbox = QHBoxLayout()
        tool_button_icon_path = "./assets/copy_white.svg" if self.night_mode_on else "./assets/copy_black.svg"
        icon = QIcon(tool_button_icon_path)
        
        num = QLabel(f"{str(count).zfill(2)} ")
        num_color = "#9ecd16" if self.night_mode_on else "#FF4400"
        num.setStyleSheet(f"color: {num_color};")
        
        word = QLabel(word)
        word.setMinimumWidth(100)
        
        copy = QToolButton()
        copy.setIcon(icon)
        copy.setIconSize(QSize(20, 20))
        
        view = QCheckBox()
        
        hspacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        hbox.addWidget(num)
        hbox.addWidget(word)
        hbox.addItem(hspacer)
        hbox.addWidget(copy)
        hbox.addWidget(view)
        
        frame: QFrame = QFrame()
        frame.setObjectName("view_frame")
        frame.setStyleSheet("QFrame#view_frame{border: 2px solid #005BC6;border-radius: 5px;}")
        frame.setLayout(hbox)
        
        return frame
        