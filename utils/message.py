import sys
import os
from functools import reduce

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from PyQt5.QtWidgets import QMessageBox

from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton

styles = [
    Label,
    Dialog,
    PushButton,
]




class Message(QMessageBox):
    def __init__(self, message, title):
        super(Message, self).__init__()
        self.setIcon(QMessageBox.Warning)
        self.setText(message)
        self.setWindowTitle(title)
        self.setStyleSheet(reduce(lambda a, b: a + b, styles))
    
    def create(self):
        return self