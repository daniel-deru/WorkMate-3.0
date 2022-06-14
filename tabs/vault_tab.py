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
        self.chk_delete.clicked.connect(self.checkHandler)
        self.chk_edit.clicked.connect(self.checkHandler)
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

    def checkHandler(self):
        edit = self.chk_edit
        delete = self.chk_delete

        if edit.isChecked():
            delete.setChecked(False)
        elif delete.isChecked():
            edit.setChecked(False)

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
            app_secret.exec_()
        elif signal == "crypto":
            new_crypto_secret = CryptoVaultWindow()
            new_crypto_secret.exec_()
    
    def create_secrets(self):
        secrets = Model().read('vault')

        crypto_container = self.vbox_crypto_vault
        app_container = self.vbox_app_vault
        general_container = self.vbox_general_vault

        for secret in secrets:

            vault_item = VaultItem(secret).create()
            vault_item.vault_clicked_signal.connect(self.get_secret)

            if(secret[1] == "crypto"):
                crypto_container.addWidget(vault_item)
            elif secret[1] == "app":
                app_container.addWidget(vault_item)
            elif secret[1] == "general":
                general_container.addWidget(vault_item)
        
    # Main event handler for when a button is clicked
    def get_secret(self, secret):
        edit = self.chk_edit
        delete = self.chk_delete
        if delete.isChecked():
            self.delete_secret(secret)
        elif edit.isChecked():
            self.edit_secret(secret)

        # Replace this
        if(secret[1] == "app"):
            self.app_vault_click(secret)
        elif secret[1] == "crypto":
            self.crypto_vault_click(secret)
        elif secret[1] == "general":
            self.general_vault_click(secret)
        # Allow Opening the app without loggin in
        if (secret[1] == "app") and not (edit.isChecked() or delete.isChecked()):
            data = json.loads(secret[3])
            try:
                os.startfile(data['path'])
            except OSError:
                pass
        # Prompt user to log in if not logged in
        elif not self.logged_in:
            self.login_clicked()
        elif not edit.isChecked() and not delete.isChecked() and self.logged_in:
            protected_view = ProtectedView(secret, 'secret')
            protected_view.exec_()
        elif delete.isChecked() and self.logged_in:
            Model().delete('vault', secret[0])
            self.update()
            # Set the delete check button to off after an app has been deleted
            delete.setChecked(False)
        # elif edit.isChecked() and self.logged_in:
        #     secret_edit_window = SecretWindow(secret)
        #     secret_edit_window.secret_signal.connect(lambda: self.update())
        #     secret_edit_window.exec_()
            # Set the Edit checkbox to off after the secret has been edited
            self.chk_edit.setChecked(False)
    
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
        else:
            if not self.logged_in:
                self.login_clicked()
            else:
                if edit.isChecked():
                    pass
                    # edit the app
                elif delete.isChecked():
                    pass
                    # delete the app

    def crypto_vault_click(self, secret):
        pass

    def general_vault_click(self, secret):
        pass

    def delete_secret(self, secret):
        if not self.logged_in:
            self.login_clicked()
        else:
            Model().delete("vault", secret[0])
            self.update()
    
    def edit_secret(self, secret):
        if not self.logged_in:
            self.login_clicked()
        else:
            if secret[1] == "app":
                pass
                # Open the app edit window
            elif secret[1] == "crypto":
                crypto_vault_window = CryptoVaultWindow(secret)
                crypto_vault_window.exec_()
                # open the crypto edit window
            elif secret[1] == "general":
                pass
                # Open edit general window
            
    