import sys
import os

from winsound import PlaySound
import winsound

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.reset_password import Ui_ResetPassword

from utils.helpers import StyleSheet

from widgetStyles.Dialog import Dialog
from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.PushButton import PushButton

from database.model import Model


class ResetPassword(Ui_ResetPassword, QDialog):
    def __init__(self):
        super(ResetPassword, self).__init__()
        self.setupUi(self)
        self.read_styles()

        self.btn_reset.clicked.connect(self.compare_passwords)

    def read_styles(self):
        widgetlist: list[str] = [
            Dialog,
            Label,
            LineEdit,
            PushButton
        ]

        stylesheet: str = StyleSheet(widgetlist).create()
        self.setStyleSheet(stylesheet)

    def compare_passwords(self):
        pass1 = self.lnedt_password1.text()
        pass2 = self.lnedit_confirm_password.text()

        if(pass1 != pass2):
            self.lbl_message.setText("The passwords don't match")
            PlaySound("sound.wav", winsound.SND_FILENAME)
        else:
            Model().update('user', {'password': pass1}, 'user')
            self.close()
            