import os
import sys

from widgetStyles.Label import Label
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QFont

from widgetStyles.PushButton import PushButton
from widgetStyles.Dialog import Dialog

from utils.helpers import StyleSheet

from database.model import Model


class PassphraseCopyWindow(QDialog):
    yes_signal = pyqtSignal(bool)
    def __init__(self) -> None:
        super(PassphraseCopyWindow, self).__init__()
        self.setupUi()
        self.setFixedHeight(300)
        self.setWindowTitle("Are you sure?")
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.read_styles()
        
        self.btn_no.clicked.connect(lambda: self.response(False))
        self.btn_yes.clicked.connect(lambda: self.response(True))
        
    def read_styles(self):
        widget_list = [
            Dialog,
            PushButton
        ]
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_name = Model().read("settings")[0][2]
        
        font_list = [
            self.lbl_message,
            self.btn_no,
            self.btn_yes
        ]
        
        for item in font_list:
            item.setFont(QFont(font_name))
    
    def setupUi(self):
        vbox: QVBoxLayout = QVBoxLayout()
        
        self.lbl_message: QLabel = QLabel("DID YOU STORE YOUR PASSPHRASE IN A SAFE PLACE?")
        self.lbl_message.setStyleSheet("color: red;font-size: 30px;")
        self.lbl_message.setAlignment(Qt.AlignCenter)
        self.lbl_message.setWordWrap(True)
        
        hbox_btn_container: QHBoxLayout = QHBoxLayout()
        
        self.btn_yes: QPushButton = QPushButton("Yes")
        self.btn_no: QPushButton = QPushButton("No")
        
        hbox_btn_container.addWidget(self.btn_yes)
        hbox_btn_container.addWidget(self.btn_no)
        
        vbox.addWidget(self.lbl_message)
        vbox.addLayout(hbox_btn_container)
        
        self.setLayout(vbox)
    
    def response(self, response):
        self.close()
        self.yes_signal.emit(response)
        return response