import sys
import os
from functools import reduce

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from PyQt5.QtWidgets import QMessageBox

from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton
from utils.helpers import StyleSheet






class Message(QMessageBox):
    def __init__(self, message, title):
        super(Message, self).__init__()
        self.setIcon(QMessageBox.Warning)
        self.setText(message)
        self.setWindowTitle(title)
        styles = [
            Label,
            Dialog,
            PushButton,
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
    
    def create(self):
        return self