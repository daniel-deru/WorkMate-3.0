import os
import sys

from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.login_window import Ui_Login
from utils.helpers import StyleSheet
from database.model import Model
from utils.message import Message
import assets.resources

from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.PushButton import PushButton
from widgetStyles.Dialog import Dialog


class Login(QDialog, Ui_Login):
    login_status = pyqtSignal(str)
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/WorkMate.ico"))
        self.read_styles()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.btn_login.clicked.connect(self.login)
        self.lnedt_password.setEchoMode(QLineEdit.Password)


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
        user = Model().read("user")[0]
        db_password = user[3]
        password = self.lnedt_password.text()
        if(password == db_password):
            self.login_status.emit("success")
            self.close()
        else:
            Message("The password is incorrect", "Wrong Password").exec_()
            self.login_status.emit("failure")