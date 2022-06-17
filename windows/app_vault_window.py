import sys
import os
from json import dumps

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.app_vault_window import Ui_AppVault

from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label
from widgetStyles.SpinBox import SpinBox

from utils.helpers import StyleSheet, json_to_dict
from utils.message import Message

from database.model import Model

class AppVaultWindow(Ui_AppVault, QDialog):
    app_update_signal = pyqtSignal(bool)
    def __init__(self, app=None):
        super(Ui_AppVault, self).__init__()
        self.app = app
        self.setupUi(self)

        if self.app:
            self.fill_data()
        self.read_styles()


        self.btn_save.clicked.connect(self.save)

    def read_styles(self):
        widget_list = [
            Label,
            Dialog,
            PushButton,
            LineEdit,
            SpinBox
        ]

        stylesheet: str = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)

    def save(self):
        name: str = self.lne_name.text()
        index: str = self.spn_index.text()
        path: str = self.lne_path.text()

        username: str = self.lne_username.text()
        email: str = self.lne_email.text()
        password: str = self.lne_password.text()

        name_list: list[str] = ["name", "index", "path", "username", "email", "password"]
        data_list: list[str] = [ name, index, path, username, email, password ]

        valid_submit: bool = True

        for i in range(len(data_list)):
            if(not data_list[i]):
                Message(f"Please add {name_list[i]}", f"Missing {name_list[i]}").exec_()
                valid_submit = False

        if valid_submit:
            data: str = dumps({
                'name': name,
                'sequence': index,
                'path': path,
                'username': username,
                'email': email,
                'password': password
            })

            if self.app:
                Model().update("vault", {'type': 'app', 'name': name, 'data': data}, self.app[0])
            else:
                Model().save("vault", {'type': "app", 'name': name, 'data': data })
                
            self.app_update_signal.emit(True)
            self.close()
    
    def fill_data(self):
        data: object = json_to_dict(self.app[3])
        
        self.lne_name.setText(data['name'])
        self.lne_password.setText(data['password'])
        self.lne_email.setText(data['email'])
        self.lne_username.setText(data['username'])
        self.lne_path.setText(data['path'])
        self.spn_index.setValue(int(data['sequence']))