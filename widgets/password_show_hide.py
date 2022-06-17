import os
import sys

from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QToolButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from colorama import Style


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.Widget import Widget
from widgetStyles.LineEdit import LineEdit
from widgetStyles.ToolButton import ToolButton

from utils.helpers import StyleSheet

class PasswordWidget(QWidget):
    def __init__(self, input=None):
        super(PasswordWidget, self).__init__()
        self.input = input
        self.createWidget()
        self.read_styles()
        self.returnWidget()

    def createWidget(self):
        hbox: QHBoxLayout = QHBoxLayout()

        self.text_field: QLineEdit = QLineEdit()
        if(self.input):
            self.text_field.setText(self.input)
        self.show_button: QToolButton = QToolButton()
        self.show_button.setIcon(QIcon("./assets/eye_white_open.svg"))
        self.show_button.clicked.connect(self.show_hide_password)

        hbox.addWidget(self.text_field)
        hbox.addWidget(self.show_button)

        self.setLayout(hbox)
        self.setMinimumWidth(200)

    def show_hide_password(self):
        if self.text_field.echoMode() == QLineEdit.Normal:
            self.text_field.setEchoMode(QLineEdit.Password)
            self.show_button.setIcon(QIcon("./assets/eye_white_closed.svg"))
        else:
            self.text_field.setEchoMode(QLineEdit.Normal)
            self.show_button.setIcon(QIcon("./assets/eye_white_open.svg"))
    
    def returnWidget(self):
        return self

    def read_styles(self):
        widget_list = [
            Widget,
            LineEdit,
            ToolButton
        ]
        stylesheet: str = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
    