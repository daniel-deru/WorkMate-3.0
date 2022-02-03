import os
import sys
import math

from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from windows.protected_view_window import ProtectedView


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_tab import Ui_Vault_tab

from utils.helpers import StyleSheet
from utils.message import Message
from utils.helpers import clear_window

from widgets.vault_item import VaultItem

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
        self.create_secrets()

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
        new_secret.secret_signal.connect(self.update)
        new_secret.exec_()
    
    def create_secrets(self):
        apps = Model().read('vault')
        COLUMNS = 5
        sorted_secrets = sorted(apps, key=lambda item: item[3])
        grid_items = []
        # Create the grid for the layout
        for i in range(math.ceil(len(sorted_secrets)/COLUMNS)):
            subarr = []
            for j in range(COLUMNS):
                if sorted_secrets:
                    subarr.append(sorted_secrets.pop(0))
            grid_items.append(subarr)

        # Add the items to the layout
        for i in range(len(grid_items)):
            row = i
            for j in range(len(grid_items[i])):
                col = j
                app_button = VaultItem(grid_items[i][j]).create()
                # connect to signal when button is clicked
                app_button.vault_clicked_signal.connect(self.get_secret)
                self.gbox_secret.addWidget(app_button, row, col)
        
    def get_secret(self, secret):
        protected_view = ProtectedView(secret, 'secret')
    
    def update(self):
        clear_window(self.gbox_secret)
        self.create_secrets()
        self.read_styles()
            
    