import os
import sys

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.login_window import Ui_Login
from utils.helpers import StyleSheet
from database.model import Model
from utils.message import Message

from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.PushButton import PushButton
from widgetStyles.Dialog import Dialog


class Login(QDialog, Ui_Login):
    login_status = pyqtSignal(str)
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.read_styles()


    def read_styles(self):
        styles = [
            PushButton,
            Label,
            LineEdit,
            Dialog
            ]
        
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)

    def login(self):
        user = Model().read("user")
        db_password = user[2]
        password = self.lnedt_password.text()

        if(password == db_password):
            self.login_status.emit("success")
            self.close()
        else:
            Message("The password is incorrect", "Wrong Password").exec_()