import json
import sys
import os
from datetime import date, datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import pyqtSignal

from designs.python.update_password import Ui_UpdatePassword

from utils.message import Message
from utils.helpers import StyleSheet

from widgetStyles.Dialog import Dialog
from widgetStyles.DateEdit import DateEditForm
from widgetStyles.PushButton import PushButton
from widgetStyles.QCheckBox import EyeCheckBox
from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Frame import FrameContainer

class UpdatePassword(Ui_UpdatePassword, QDialog):
    def __init__(self, data) -> None:
        super(UpdatePassword, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.data = data
        self.queue = [self.data.pop(-1)]
        self.dte_password_exp.setDate(date.today() + timedelta(days=90))
        self.show_item()
        
        self.btn_same.clicked.connect(self.same_password)
        
        self.chk_show_password1.stateChanged.connect(lambda state: self.show_password(state, self.lne_password1))
        self.chk_show_password2.stateChanged.connect(lambda state: self.show_password(state, self.lne_password2))
        
    def read_styles(self):
        widget_list = [
            Label,
            DateEditForm,
            Dialog,
            PushButton,
            EyeCheckBox,
            LineEdit,
            FrameContainer("#frame_account")
        ]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
    def same_password(self):
        if len(self.data) == 0: 
            return
        self.queue.pop()
        self.queue.append(self.data.pop(-1))
        self.show_item()

    def show_item(self):
        table, item = self.queue[0]
        data: object = {}
        if table == "user":
            data = self.get_user_data(item)
        else:
            data = self.get_vault_data(item)
            
        self.lbl_account_display.setText(data['account'])
        self.lbl_email_display.setText(data['email'])
            
                    
            
    def get_user_data(self, item):
        email = item[2]
        account = "Trust Lock"
        
        user_data = {
            'email': email,
            'account': account
        }
        
        return user_data
    
    def get_vault_data(self, item):
        json_data = json.loads(item[3])
        email = json_data['email']
        account = json_data['username']
        
        vault_data = {
            'email': email,
            'account': account
        }
        
        return vault_data
    
    def show_password(self, checked, field: QLineEdit):
        if not checked:
            field.setEchoMode(QLineEdit.Password)
        else:
            field.setEchoMode(QLineEdit.Normal)
            
        
    