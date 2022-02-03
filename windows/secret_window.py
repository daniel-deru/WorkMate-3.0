import os
import sys
import json

from PyQt5.QtWidgets import QDialog
from cryptography.fernet import Fernet

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_add_window import Ui_AddSecret_window

from database.model import Model

from widgetStyles.PushButton import PushButton
from widgetStyles.SpinBox import SpinBox
from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Dialog import Dialog

from utils.helpers import StyleSheet
from utils.message import Message


class SecretWindow(QDialog, Ui_AddSecret_window):
    def __init__(self):
        super(SecretWindow, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.btn_save.clicked.connect(self.get_data)
        self.btn_cancel.clicked.connect(lambda: self.close())

    def get_data(self):
        data = []
        fields = self.vbox_column_def.layout()

        name = self.lnedt_name.text()
        if not name:
            Message("Please enter a display name for your secret by which your will recognize it.", "No Name Entered")

        for i in range(fields.count()):
            field = fields.itemAt(i).layout()
            header_field = field.itemAt(0).widget()
            data_field = field.itemAt(1).widget()


            if not header_field.text() and data_field.text():
                Message("One or more of your data entries is missing a header. Please", "Please check your information.").exec_()
            elif header_field.text() and not data_field.text():
                Message("One or more of your header fields is missing a data entry.", "Please check your information.").exec_()
            elif header_field.text() and data_field.text():
                data.append([header_field.text(), data_field.text()])

        encrypted = self.encrypt(data)
        data = {
            'name': name,
            'data': encrypted['secret'],
            'key': encrypted['key']
        }
        Model().save('vault', data)
    
    def encrypt(self, data):
                # Convert data to json
        json_data = json.dumps(data)
        # Generate Random Key
        key = Fernet.generate_key()
        f = Fernet(key)

        # Convert the json data to bytes and encrypt with secret key
        secret = f.encrypt(json_data.encode("UTF-8"))

        return {
            'secret': secret,
            'key': key
            }



    

    def read_styles(self):
        styles = [
            PushButton,
            SpinBox,
            Label,
            LineEdit,
            Dialog
        ]

        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)