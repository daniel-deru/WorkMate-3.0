import os
import sys
from tabnanny import check

from PyQt5.QtWidgets import QDialog, QLineEdit, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QCloseEvent, QFont

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
from widgetStyles.QCheckBox import BlackEyeCheckBox, WhiteEyeCheckBox

from windows.twofa_verify_window import TwofaVerifyWindow


class Login(QDialog, Ui_Login):
    login_status = pyqtSignal(str)
    def __init__(self):
        super(Login, self).__init__()
        
        self.login_state = "failure"
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.read_styles()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        
        
        self.btn_login.clicked.connect(self.login)
        
        pass_field = self.lnedt_password
        show_pass = QLineEdit.Normal
        hide_pass = QLineEdit.Password
        show_password_callback = lambda show: pass_field.setEchoMode(show_pass) if show else pass_field.setEchoMode(hide_pass)
        self.chk_show_password.stateChanged.connect(show_password_callback)
        self.lnedt_password.setEchoMode(QLineEdit.Password)


    def read_styles(self):
        settings = Model().read('settings')[0]
        dark_mode_on = int(settings[1])
        font: str = settings[2]
        checkbox = WhiteEyeCheckBox if dark_mode_on else BlackEyeCheckBox
        
        print(dark_mode_on == True)
        print(dark_mode_on)
        print(type(dark_mode_on))
        styles = [
            PushButton,
            Label,
            LineEdit,
            Dialog,
            checkbox
            ]
        
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        font_widgets = [
            self.lbl_password,
            self.lnedt_password,
            self.btn_login
        ]
        
        widget: QWidget
        for widget in font_widgets:
            widget.setFont(QFont(font))
        

    def login(self):
        user = Model().read("user")[0]
        db_password = user[3]
        password = self.lnedt_password.text()
        if(password == db_password):
            has_2fa = Model().read('settings')[0][7]
            if(int(has_2fa)):
                self.hide()
                twofa_verify_window = TwofaVerifyWindow()
                twofa_verify_window.opt_verify_signal.connect(self.verify_otp)
                twofa_verify_window.exec_()
                # Go to the two fa login window
            else:
                self.login_status.emit("success")
                self.login_state = "success"
                self.close()
        else:
            Message("The password is incorrect", "Wrong Password").exec_()
            self.login_status.emit("failure")
            self.login_state = "failure"
    
    def verify_otp(self, verified):
        if(verified):
            self.login_status.emit("success")
            self.login_state = "success"
            self.close()
            
    def closeEvent(self, a0: QCloseEvent) -> None:
        self.login_status.emit(self.login_state)
        return super().closeEvent(a0)
    
    def show_password(self, show):
        if show: self.lnedt_password.setEchoMode(QLineEdit.Normal)
        else: self.lnedt_password.setEchoMode(QLineEdit.Password)
            
