import os
import sys
import qrcode
import pyotp
import pyperclip

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon, QCursor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.twofa_window import Ui_TwoFADialog

from utils.helpers import StyleSheet
from utils.qrcode import QRCodeTemplate

from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton100Width

from database.model import Model

class TwofaDialog(Ui_TwoFADialog, QDialog):
    def __init__(self):
        super(TwofaDialog, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setupUi(self)
        self.read_styles()
        self.create_qrcode()
        
        self.btn_copy.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.btn_copy.clicked.connect(lambda: pyperclip.copy(self.lbl_setupkey.text()))
        self.btn_exit.clicked.connect(self.close)

    def read_styles(self):
        widget_list = [Label, Dialog, PushButton100Width]

        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_name = Model().read("settings")[0][2]
        
        font_widgets =[
            self.lbl_message,
            self.lbl_setupkey
        ]
        
        widget: QWidget
        for widget in font_widgets:
            widget.setFont(QFont(font_name))

    def create_qrcode(self):
        secret = self.get_otp()
        email = Model().read("user")[0][2]
        auth_string = f"otpauth://totp/TrustLock:{email}?secret={secret}&issuer=TrustLock"

        self.lbl_qrcode.setPixmap(qrcode.make(auth_string, image_factory=QRCodeTemplate).pixmap())

    def get_otp(self):
        otp = Model().read("user")[0][5]

        if otp == None or otp == "None":
            
            otp = pyotp.random_base32()
            Model().update('user', {'twofa_key': otp}, 'user')
        self.lbl_setupkey.setText(otp)

        return otp


    