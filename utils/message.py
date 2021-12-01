import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from PyQt5.QtWidgets import QMessageBox

from styles.windows.messageWindow import message_window_styles


class Message(QMessageBox):
    def __init__(self, message, title):
        super(Message, self).__init__()
        self.setIcon(QMessageBox.Warning)
        self.setText(message)
        self.setWindowTitle(title)
        self.setStyleSheet(message_window_styles)
    
    def create(self):
        return self