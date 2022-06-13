import os
import sys

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_type_window import Ui_VaultTypeDialog

from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import ButtonFullWidth

from utils.helpers import StyleSheet

class VaultType(Ui_VaultTypeDialog, QDialog):
    vault_type_signal = pyqtSignal(str)
    def __init__(self):
        super(Ui_VaultTypeDialog, self).__init__()
        self.setupUi(self)
        self.readStyles()

        self.btn_general.clicked.connect(self.open_general_vault)
        self.btn_app.clicked.connect(self.open_app_vault)
        self.btn_crypto.clicked.connect(self.open_crypto_vault)

    def readStyles(self):
        widget_list = [ButtonFullWidth, Dialog]

        stylesheet = StyleSheet(widget_list).create()

        self.setStyleSheet(stylesheet)

    def open_general_vault(self):
        self.vault_type_signal.emit("general")
        self.close()

    def open_app_vault(self):
        self.vault_type_signal.emit("app")
        self.close()

    def open_crypto_vault(self):
        self.vault_type_signal.emit("crypto")
        self.close()

