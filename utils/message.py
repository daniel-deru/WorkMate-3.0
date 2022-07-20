import sys
import os

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton
from utils.helpers import StyleSheet

from database.model import Model


class Message(QMessageBox):
    def __init__(self, message, title, label_style=None):
        super(Message, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint);
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setIcon(QMessageBox.Warning)
        self.setText(message)
        self.setWindowTitle(title)
        
        # Find the custom style or use the default styles
        label = label_style if label_style else Label 
        styles = [
            label,
            Dialog,
            PushButton,
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        font_name = Model().read("settings")[0][2]
        self.setFont(QFont(font_name))
    
    def create(self):
        return self
    
    def prompt(self, buttons=QMessageBox.Yes | QMessageBox.No):
        self.setStandardButtons(buttons)
        return self.exec_()