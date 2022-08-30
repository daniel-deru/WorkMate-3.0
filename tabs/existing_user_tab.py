import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import math

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QIcon, QFont

from designs.python.existing_user_tab import Ui_ExistingUser

from utils.helpers import set_font, StyleSheet

from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.ToolButton import ToolButton
from widgetStyles.PushButton import PushButton

from database.model import Model

class ExistingUserTab(Ui_ExistingUser, QWidget):
    def __init__(self) -> None:
        super(ExistingUserTab, self).__init__()
        self.setupUi(self)
        
        self.set_style()
        self.set_icons()
        self.create_key_inputs()
        
    def create_key_inputs(self):
        keys_num: int = 12
        cols: int = 4
        count = 1
        font_name = Model().read("settings")[0][2]
        font = QFont(font_name)
        
        for i in range(math.ceil(keys_num/cols)):
            for j in range(cols):
                hbox = QHBoxLayout()
                lbl_num = QLabel(f"{str(count).zfill(2)}.")
                lne_key = QLineEdit()
                
                lbl_num.setFont(font)
                lne_key.setFont(font)
                
                hbox.addWidget(lbl_num)
                hbox.addWidget(lne_key)
                self.gbox_keys.addLayout(hbox, i, j)
                count += 1
        
    def set_icons(self):
        self.tbtn_database.setIcon(QIcon(":/button_icons/database"))
        self.tbtn_key_file.setIcon(QIcon(":/button_icons/key_file"))
        
    def create_tab(self):
        return self
    
    def set_style(self):
        style_list = [
            Label
        ]
        
        stylesheet = StyleSheet(style_list).create()
        self.setStyleSheet(stylesheet)
        
        widget_list = [
            self.lbl_database,
            self.lbl_key_file,
            self.lbl_keys,
            self.lne_key_file,
            self.lne_database,
            self.btn_create
        ]
        
        set_font(widget_list)