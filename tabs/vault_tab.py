import os
import sys
import json
import math

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_tab import Ui_Vault_tab

from utils.helpers import StyleSheet, json_to_dict
from utils.helpers import clear_window

from widgets.vault_item import VaultItem
from widgets.filter_group_widget import FilterGroupWidget

from windows.secret_window import SecretWindow
from windows.crypto_vault_window import CryptoVaultWindow
from windows.app_vault_window import AppVaultWindow

from windows.vault_type_window import VaultType

from windows.app_vault_view_window import AppVaultView
from windows.crypto_vault_view_window import CryptoVaultViewWindow
from windows.general_vault_view_window import GeneralVaultView

from widgetStyles.QCheckBox import CheckBoxSquare
from widgetStyles.PushButton import PushButton, VaultButton
from widgetStyles.Label import Label
from widgetStyles.ScrollArea import ScrollArrea
from widgetStyles.ScrollBar import ScrollBar
from widgetStyles.ComboBox import ComboBox

from database.model import Model

class Vault_tab(Ui_Vault_tab, QWidget):
    vault_signal = pyqtSignal(str)
    login_signal = pyqtSignal(str)
    def __init__(self):
        super(Vault_tab, self).__init__()
        self.setupUi(self)
        
        self.filter_widget = FilterGroupWidget()
        self.filter_widget.group_changed_signal.connect(lambda group: self.create_secrets(group))
        self.hbox_filter_widget.addWidget(self.filter_widget)
        self.read_styles()
        
        initial_group = self.filter_widget.get_current_group()
        self.create_secrets(initial_group)

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
            CheckBoxSquare,
            Label,
            ScrollArrea,
            ScrollBar,
            ComboBox
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
    
    def create_secrets(self, group):
        clear_window(self.gbox_secrets)
        secrets = Model().read('vault')
        
        current_group = list(filter(lambda todo: todo[4] == str(group), secrets))
        print(current_group)
            
        COLUMNS = 4
        grid_items = []
        for i in range(math.ceil(len(current_group)/COLUMNS)):
            subarr = []
            for j in range(COLUMNS):
                if current_group:
                    subarr.append(current_group.pop(0))
            grid_items.append(subarr)
            
        for i in range(len(grid_items)):
            row = i
            for j in range(len(grid_items[i])):
                col = j
                self.secret_item = VaultItem(grid_items[i][j]).create()
                self.secret_item.vault_clicked_signal.connect(self.update)
                self.gbox_secrets.addWidget(self.secret_item, row, col)
        
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
        clear_window(self.gbox_secrets)
        initial_group = self.filter_widget.get_current_group()
        self.create_secrets(initial_group)
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
            self.btn_login.setText("Login")
            self.logged_in = False

    def display_apps(self):
        apps = Model().read('appvault')
    
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
            return
        else:
            Model().delete("vault", secret[0])
            self.chk_delete.setChecked(False)
            self.update()
    
    def edit_secret(self, secret):
        if not self.logged_in:
            self.login_clicked()
            return
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
        if not self.logged_in:
            self.login_clicked()
            return
        if secret[1] == "app":
            app_view = AppVaultView(secret)
            app_view.exec_()
        elif secret[1] == "crypto":
            crypto_vault = CryptoVaultViewWindow(secret)
            crypto_vault.exec_()
        elif secret[1] == "general":
            general_vault = GeneralVaultView(secret)
            general_vault.exec_()
