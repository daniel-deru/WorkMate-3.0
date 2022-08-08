import os
import sys

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_type_window import Ui_VaultTypeDialog

from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import ButtonFullWidth, VaultButton
from widgetStyles.styles import VAULT_BUTTON_COLORS

from utils.helpers import StyleSheet

from database.model import Model

class VaultType(Ui_VaultTypeDialog, QDialog):
    vault_type_signal = pyqtSignal(str)
    def __init__(self):
        super(Ui_VaultTypeDialog, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setupUi(self)
        self.readStyles()

        self.btn_general.clicked.connect(self.open_general_vault)
        self.btn_app.clicked.connect(self.open_app_vault)
        self.btn_crypto.clicked.connect(self.open_crypto_vault)

    def readStyles(self):
        widget_list = [ButtonFullWidth, Dialog]

        stylesheet = StyleSheet(widget_list).create()

        self.setStyleSheet(stylesheet)
        
        font_name = Model().read("settings")[0][2]
        
        font_widget = [
            self.btn_app,
            self.btn_crypto,
            self.btn_general
        ]
        self.btn_app.setStyleSheet(f"background-color: {VAULT_BUTTON_COLORS['app']};border: 1px solid {VAULT_BUTTON_COLORS['app']};")
        self.btn_crypto.setStyleSheet(f"background-color: {VAULT_BUTTON_COLORS['crypto']};border: 1px solid {VAULT_BUTTON_COLORS['crypto']};")
        self.btn_general.setStyleSheet(f"background-color: {VAULT_BUTTON_COLORS['general']};border: 1px solid {VAULT_BUTTON_COLORS['general']};")        
        
        widget: QWidget
        
        for widget in font_widget:
            widget.setFont(QFont(font_name))

    def open_general_vault(self):
        self.vault_type_signal.emit("general")
        self.close()

    def open_app_vault(self):
        self.vault_type_signal.emit("app")
        self.close()

    def open_crypto_vault(self):
        self.vault_type_signal.emit("crypto")
        self.close()

