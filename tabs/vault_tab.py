import os
import sys
import pyperclip

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_tab import Ui_Vault_tab
from utils.helpers import StyleSheet
from utils.message import Message

from windows.secret_window import SecretWindow

from widgetStyles.QCheckBox import CheckBox
from widgetStyles.PushButton import PushButton

from database.model import Model

class Vault_tab(QWidget, Ui_Vault_tab):
    vault_signal = pyqtSignal(str)
    def __init__(self):
        super(Vault_tab, self).__init__()
        self.setupUi(self)
        self.read_styles()

        self.btn_add.clicked.connect(self.add_clicked)
       
        self.vault_signal.connect(self.update)

        self.logged_in = False

    def create_tab(self):
        return self

    def read_styles(self):
        styles = [
            PushButton,
            CheckBox
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)

    def add_clicked(self):
        new_secret = SecretWindow()
        new_secret.exec_()
    