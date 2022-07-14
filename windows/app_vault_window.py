import sys
import os
from json import dumps

from PyQt5.QtWidgets import QDialog, QFileDialog, QLineEdit, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

from designs.python.app_vault_window import Ui_AppVault

from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label
from widgetStyles.SpinBox import SpinBox

from utils.helpers import StyleSheet, json_to_dict, get_checkbox
from utils.message import Message

from database.model import Model

class AppVaultWindow(Ui_AppVault, QDialog):
    app_update_signal = pyqtSignal(bool)
    def __init__(self, app=None):
        super(Ui_AppVault, self).__init__()
        self.app = app
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.secrets = list(filter(lambda a: a[1] == "app", Model().read("vault")))
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        
        maxValue = len(self.secrets) if self.app else len(self.secrets)+1
        
        self.spn_index.setMaximum(maxValue)
        self.spn_index.setValue(maxValue)
        self.spn_index.setMinimum(1)
        self.lne_password.setEchoMode(QLineEdit.Password)
        

        if self.app: self.fill_data()
        
        self.read_styles()
        self.btn_save.clicked.connect(self.save)
        self.btn_desktop.clicked.connect(self.add_from_desktop)
        
        self.chk_show_password.stateChanged.connect(lambda show: self.show_password(show, self.lne_password))
        self.chk_password2.stateChanged.connect(lambda show: self.show_password(show, self.lne_password2))
        

    def read_styles(self):
        checkbox = get_checkbox()
        widget_list = [
            Label,
            Dialog,
            PushButton,
            LineEdit,
            SpinBox,
            checkbox
        ]

        stylesheet: str = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_name = Model().read("settings")[0][2]
        
        font_widget = [
            self.lbl_email,
            self.lbl_index,
            self.lbl_name,
            self.lbl_password,
            self.lbl_path,
            self.lbl_username,
            self.lne_email,
            self.spn_index,
            self.lne_name,
            self.lne_password,
            self.lne_path,
            self.lne_username,
            self.btn_desktop,
            self.btn_save
        ]
        
        widget: QWidget
        
        for widget in font_widget:
            widget.setFont(QFont(font_name))

    def save(self):
        
        name: str = self.lne_name.text()
        index: str = self.spn_index.text()
        path: str = self.lne_path.text()

        username: str = self.lne_username.text()
        email: str = self.lne_email.text()
        password: str = self.lne_password.text()
        confirm_password: str = self.lne_password2

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
            
            if password != confirm_password:
                Message("The password and confirm password are not the same.", "Passwords don't match").exec_()
                return "Stop this method from further execution"
            
            if int(index) <= len(self.secrets):
                self.update_sequence(str(index))

            if self.app:
                Model().update("vault", {'type': 'app', 'name': name, 'data': data}, self.app[0])
            else:
                Model().save("vault", {'type': "app", 'name': name, 'data': data })
                
                
                
            self.app_update_signal.emit(True)
            self.close()
    
    def fill_data(self):
        
        self.btn_save.setText("Update")
        self.setWindowTitle("Update App")
        
        data: object = json_to_dict(self.app[3])
        
        self.lne_name.setText(data['name'])
        self.lne_password.setText(data['password'])
        self.lne_email.setText(data['email'])
        self.lne_username.setText(data['username'])
        self.lne_path.setText(data['path'])
        self.spn_index.setValue(int(data['sequence']))
        
    def add_from_desktop(self):
        file = QFileDialog.getOpenFileName(self, "Open a file", DESKTOP, "All Files (*.*)")[0]
        self.lne_path.setText(file)
        
    def update_sequence(self, index: str):
        # Get the app that needs to be updated
        update_app = list(filter(lambda a: json_to_dict(a[3])['sequence'] == index, self.secrets))[0]
        # Get the data from the app that needs to be updated
        update_app_data = json_to_dict(update_app[3])
        # The app was edited
        if self.app:
            # Get the data from the current app being updated
            data = json_to_dict(self.app[3])
            # Get the sequence to put in the app the needs to be updated
            new_sequence = data['sequence']
            update_app_data['sequence'] = new_sequence
            Model().update("vault", {'data': dumps(update_app_data)}, update_app[0])
        # It's a new app
        else:
            # its a new app
            update_app_data['sequence'] = str(len(self.secrets)+1)
            Model().update("vault", {'data': dumps(update_app_data)}, update_app[0])
            
    def show_password(self, show, field):
        if show: field.setEchoMode(QLineEdit.Normal)
        else: field.setEchoMode(QLineEdit.Password)