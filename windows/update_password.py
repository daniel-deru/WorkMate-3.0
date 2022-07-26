import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal

from designs.python.update_password import Ui_UpdatePassword

from utils.message import Message

class UpdatePassword(Ui_UpdatePassword, QDialog):
    def __init__(self, email, password, account="Trust Lock", type="user") -> None:
        super(UpdatePassword, self).__init__()
        self.setupUi(self)
        
        self.lbl_account_display.setText(account)
        self.lbl_email_display.setText(email)
        
    