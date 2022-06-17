from ctypes import alignment
import os
import sys
import math
import json

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
from windows.crypto_vault_window import CryptoVaultWindow
from windows.app_vault_window import AppVaultWindow
from windows.vault_type_window import VaultType
from windows.app_vault_view_window import AppVaultView

from widgetStyles.QCheckBox import CheckBox
from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label

from database.model import Model

class Vault_tab(QWidget, Ui_Vault_tab):
    vault_signal = pyqtSignal(str)
    login_signal = pyqtSignal(str)
    def __init__(self):
        super(Vault_tab, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.create_secrets()

        self.btn_add.clicked.connect(self.add_clicked)
        self.chk_delete.clicked.connect(self.deleteCheckHandler)
        self.chk_edit.clicked.connect(self.editCheckHandler)
        self.btn_login.clicked.connect(self.login_clicked)
       
        self.vault_signal.connect(self.update)
        self.login_signal.connect(self.login)

        self.logged_in = False

    def create_tab(self):
        return self

    def read_styles(self):
        font = Model().read('settings')[0][2]
        styles = [
            PushButton,
            CheckBox,
            Label
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)

        widget_list = [
            self.chk_delete,
            self.chk_edit,
            self.btn_add,
            self.btn_login
        ]

        for widget in widget_list:
            widget.setFont(QFont(font))

    def deleteCheckHandler(self):
        self.chk_edit.setChecked(False)
            
    def editCheckHandler(self):
        self.chk_delete.setChecked(False)

    def add_clicked(self):
        vault_type = VaultType()
        vault_type.vault_type_signal.connect(self.open_vault)
        vault_type.exec_()

    
    def open_vault(self, signal):
        if(signal == "general"):
            new_secret = SecretWindow()
            new_secret.secret_signal.connect(self.update)
            new_secret.exec_()
        elif signal == "app":
            app_secret = AppVaultWindow()
            app_secret.app_update_signal.connect(self.update)
            app_secret.exec_()
        elif signal == "crypto":
            new_crypto_secret = CryptoVaultWindow()
            new_crypto_secret.crypto_update_signal.connect(self.update)
            new_crypto_secret.exec_()
    
    def create_secrets(self):
        secrets = Model().read('vault')

        crypto_container = self.vbox_crypto_vault
        app_container = self.vbox_app_vault
        general_container = self.vbox_general_vault

        for secret in secrets:

            vault_item = VaultItem(secret).create()
            vault_item.vault_clicked_signal.connect(self.get_secret)
            align = Qt.AlignCenter
            if(secret[1] == "crypto"):
                crypto_container.addWidget(vault_item, alignment=align)
            elif secret[1] == "app":
                app_container.addWidget(vault_item, alignment=align)
            elif secret[1] == "general":
                general_container.addWidget(vault_item, alignment=align)
        
    # Main event handler for when a button is clicked
    def get_secret(self, secret):
        edit = self.chk_edit
        delete = self.chk_delete
        
        if delete.isChecked():
            # Delete the secret that was clicked
            self.delete_secret(secret)
        elif edit.isChecked():
            # Edit the secret that was clicked
            self.edit_secret(secret)
        else:
            # Open the secret in view mode
            self.open_secret(secret)
    
    # Clear the window from the data add the data back and read the styles
    def update(self):
        clear_window(self.vbox_app_vault)
        clear_window(self.vbox_crypto_vault)
        clear_window(self.vbox_general_vault)
        self.create_secrets()
        self.read_styles()

    # Slot for when the login button is clicked
    def login_clicked(self):
        if self.logged_in:
            self.login_signal.emit("logout requested")
        elif not self.logged_in:
            self.login_signal.emit("login requested")

    # Slot for the login signal and middleware event handler to check if the user is logged in when an event is triggered
    def login(self, signal):
        if signal == "logged in":
            self.btn_login.setText("Logout")
            self.logged_in = True
        elif signal == "logged out":
            self.btn_login.setText("login")
            self.logged_in = False

    def display_apps(self):
        apps = Model().read('appvault')
        print(apps)
    
    def app_vault_click(self, secret):
        edit = self.chk_edit
        delete = self.chk_delete
        if not (edit.isChecked() or delete.isChecked()):
            data = json.loads(secret[3])
            try:
                os.startfile(data['path'])
            except OSError:
                pass

    def delete_secret(self, secret):
        if not self.logged_in:
            self.login_clicked()
        else:
            Model().delete("vault", secret[0])
            self.update()
            self.chk_edit.setChecked(False)
    
    def edit_secret(self, secret):
        if not self.logged_in:
            self.login_clicked()
        else:
            if secret[1] == "app":
                edit_app = AppVaultWindow(secret)
                edit_app.app_update_signal.connect(self.update)
                edit_app.exec_()
            elif secret[1] == "crypto":
                crypto_vault_window = CryptoVaultWindow(secret)
                crypto_vault_window.crypto_update_signal.connect(self.update)
                crypto_vault_window.exec_()
                # open the crypto edit window
            elif secret[1] == "general":
                general_vault_window = SecretWindow(secret)
                general_vault_window.secret_signal.connect(self.update)
                general_vault_window.exec_()
            self.chk_edit.setChecked(False)
    
    def open_secret(self, secret: tuple):
        if secret[1] == "app":
            app_view = AppVaultView(secret)
            app_view.exec_()
            
    