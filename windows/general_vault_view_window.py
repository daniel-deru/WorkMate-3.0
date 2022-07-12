import sys
import os
from json import dumps

from PyQt5.QtWidgets import QDialog, QLabel, QSpacerItem, QSizePolicy, QToolButton, QCheckBox, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QIcon, QCursor, QFont
import pyperclip

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.general_vault_view_window import Ui_GeneralVaultView

from widgetStyles.Label import Label
from widgetStyles.ToolButton import ToolButton
from widgetStyles.QCheckBox import WhiteEyeCheckBox, BlackEyeCheckBox
from widgetStyles.Dialog import Dialog

from utils.helpers import StyleSheet, json_to_dict

from database.model import Model

class GeneralVaultView(Ui_GeneralVaultView, QDialog):
    def __init__(self, secret) -> None:
        super(GeneralVaultView, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        settings = Model().read('settings')[0]
        self.night_mode_on = int(settings[1])
        self.font_name = settings[2]
        self.secret = secret
        self.data = json_to_dict(secret[3])
        self.setupUi(self)
        self.read_styles()
        self.set_data()
        

        
    def read_styles(self):
        checkbox = WhiteEyeCheckBox if self.night_mode_on else BlackEyeCheckBox
        widget_list = [
            checkbox,
            Label,
            ToolButton,
            Dialog
        ]
        
        stylesheet = StyleSheet(widget_list).create()
        
        self.setStyleSheet(stylesheet)
        
        self.lbl_description.setFont(QFont(self.font_name))
        
    def set_data(self):
        self.lbl_description.setText(self.secret[2])
        
        keys: list[str] = list(self.data.keys())
        values: list[str] = list(self.data.values())
        
        for i in range(len(keys)):
            widget = self.create_widget(keys[i], values[i])
            self.vbox_secrets.addWidget(widget)
        
    def create_widget(self, key: str, value: str) -> QFrame:
        frame: QFrame = QFrame()
        frame.setObjectName("view_frame")
        hbox = QHBoxLayout()
        
        lbl_key: QLabel = QLabel(key)
        lbl_key.setFont(QFont(self.font_name))
        lbl_key.setMinimumWidth(200)
        
        lbl_value: QLabel = QLabel(u"\u2022"*10)
        lbl_value.setFont(QFont(self.font_name))
        
        hspacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        btn_copy: QToolButton = QToolButton()
        icon_path = "./assets/copy_white.svg" if self.night_mode_on else "./assets/copy_black.svg"
        btn_copy.setIcon(QIcon(icon_path))
        btn_copy.setIconSize(QSize(20, 20))
        btn_copy.setCursor(QCursor(Qt.PointingHandCursor))
        btn_copy.clicked.connect(lambda: self.copy(key))
        
        btn_view: QCheckBox = QCheckBox()
        btn_view.setCursor(QCursor(Qt.PointingHandCursor))
        btn_view.stateChanged.connect(lambda checked: self.view(key, checked, lbl_value))
        
        hbox.addWidget(lbl_key)
        hbox.addWidget(lbl_value)
        hbox.addItem(hspacer)
        hbox.addWidget(btn_copy)
        hbox.addWidget(btn_view)
        
        vbox: QVBoxLayout = QVBoxLayout()
        
        hline: QFrame = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        hline.setStyleSheet("background: #9ecd16;")
        hline.setMaximumHeight(1)
        
        vbox.addLayout(hbox)
        vbox.addWidget(hline)
        
        frame.setLayout(vbox)
        return frame
    
    def copy(self, field_name):
        pyperclip.copy(self.data[field_name])
        
    def view(self, key: str, checked: bool, lbl_value: QLabel):
        if checked:
            lbl_value.setText(self.data[key])
        else:
            lbl_value.setText(u"\u2022"*10)
        
        
        