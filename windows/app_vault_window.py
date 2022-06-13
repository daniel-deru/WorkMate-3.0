import sys
import os

from PyQt5.QtWidgets import QDialog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.app_vault_window import Ui_AppVault

from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label
from widgetStyles.SpinBox import SpinBox

from utils.helpers import StyleSheet

class AppVaultWindow(Ui_AppVault, QDialog):
    def __init__(self):
        super(Ui_AppVault, self).__init__()
        self.setupUi(self)
        self.read_styles()

    def read_styles(self):
        widget_list = [
            Label,
            Dialog,
            PushButton,
            LineEdit,
            SpinBox
        ]

        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)