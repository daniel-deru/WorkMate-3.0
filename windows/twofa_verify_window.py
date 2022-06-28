import os
import sys
import pyotp

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.twofa_verify_window import Ui_TwofaDialog

from database.model import Model

from utils.helpers import StyleSheet

from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.PushButton import ButtonFullWidth
from widgetStyles.Dialog import Dialog

class TwofaVerifyWindow(Ui_TwofaDialog, QDialog):
    opt_verify_signal = pyqtSignal(bool)
    def __init__(self):
        super(TwofaVerifyWindow, self).__init__()  
        self.setupUi(self)
        self.read_styles()

        self.btn_verify.clicked.connect(self.verify_otp)

    def read_styles(self):
        widget_list = [ButtonFullWidth, LineEdit, Label, Dialog]

        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)

    def verify_otp(self):
        code = Model().read('user')[0][6]
        totp = pyotp.TOTP(code)
        if(totp.verify(self.lnedt_code.text())):
            self.opt_verify_signal.emit(True)
            self.close()
        else:
            self.lbl_message.setText("Invalid Code")
            self.opt_verify_signal.emit(False)
        

